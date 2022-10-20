from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from rest_framework import serializers
from core import models
from rest_framework.settings import api_settings
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
import uuid


class ImageDecode(serializers.BaseSerializer):
    def to_representation(self, value):
        if not value:
            return None

        use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
        if use_url:
            try:
                url = value.url
            except AttributeError:
                return None
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url

        return value.name

    def to_internal_value(self, data):
        if ';base64,' in data:
            header, data = data.split(';base64,')
        try:
            decoded_image = base64.b64decode(data)
        except ValueError:
            raise serializers.ValidationError('Картинка должна быть закодирована в base64')
        image_name = str(uuid.uuid4())[:10]
        uploaded = SimpleUploadedFile(
            name=image_name + '.png',
            content=decoded_image,
            content_type='recipes/'
        )
        return uploaded


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj) -> bool:
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        return user.is_subscriber(obj)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = '__all__'


class AmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = models.IngredientAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = AuthorSerializer()
    ingredients = AmountSerializer(many=True, read_only=True, source='ingredientamounts')
    image = ImageDecode()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        if obj.favorites.filter(user=user):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        if obj.shopping_carts.filter(user=user):
            return True
        return False


class TagsCreateSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return {
            'id': value.pk,
            'name': value.name,
            'color': value.color,
            'slug': value.slug,
        }

    def to_internal_value(self, data):
        data_type = type(data).__name__
        default_error_messages = {
            'required': 'This field is required.',
            'does_not_exist': f'Недопустимый pk {data} - объект не существует',
            'incorrect_type': f'Неверный тип. Ожидаемое значение pk, полученное {data_type}.',
        }
        try:
            return models.Tag.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise ValidationError(default_error_messages.get('does_not_exist'))
        except (TypeError, ValueError):
            raise ValidationError(default_error_messages.get('incorrect_type'))


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = ImageDecode()
    tags = TagsCreateSerializer(queryset=models.Tag.objects.all(), many=True)
    ingredients = AmountSerializer(many=True, source='ingredientamounts')
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientamounts')
        tags = validated_data.pop('tags')

        request = self.context['request']
        author = request.user

        recipe = models.Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
        amounts = []
        for ingredient in ingredients:
            instance = ingredient['ingredient']
            models.IngredientAmount.objects.create(
                recipe=recipe, ingredient=instance, amount=ingredient['amount']
            )
            amounts.append(instance.id)
        recipe.ingredients.set(amounts)
        return recipe

    def update(self, instance, validated_data):
        request = self.context['request']
        author = request.user
        if instance.author != author:
            raise PermissionDenied()

        ingredients = self.initial_data['ingredients']
        tags = validated_data.pop('tags')
        if validated_data.get('image'):
            instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')

        instance.tags.set(tags)
        amounts = []
        models.IngredientAmount.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            models.IngredientAmount.objects.create(
                recipe=instance, ingredient_id=ingredient_id, amount=ingredient['amount']
            )
            amounts.append(ingredient_id)

        instance.ingredients.set(amounts)

        instance.save(update_fields=[
            'image', 'name', 'text', 'cooking_time'
        ])
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = models.Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.recipe.image.url
        return request.build_absolute_uri(image_url)

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time
