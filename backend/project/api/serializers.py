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
        print(uploaded)
        print(decoded_image)
        return uploaded


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')  # , 'is_subscribed')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = AuthorSerializer()
    ingredients = IngredientSerializer(many=True)
    image = ImageDecode()

    class Meta:
        model = models.Recipe
        fields = '__all__'

    # def create(self, validated_data):
    #     print('asdsadsadsasadadss', validated_data)
    #     return validated_data


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


class IngredientsCreateSerializer(serializers.ModelSerializer):
    # id = serializers.PrimaryKeyRelatedField(queryset=models.Ingredient.objects.all())
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all()
    )
    amount = serializers.SerializerMethodField()
    # amount = serializers.IntegerField()

    class Meta:
        model = models.Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit')

    def get_amount(self, obj):
        request = self.context['request']
        data_list = request.data.get('ingredients')[0]
        amount = data_list.get('amount')
        object, status = models.IngredientAmount.objects.get_or_create(
            ingredient=obj, amount=amount
        )
        # Удалим предыдущую информацию, если такова имеется
        if status is True:
            models.IngredientAmount.objects.filter(
                ingredient=obj).exclude(amount=amount).delete()
        return amount


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = ImageDecode()
    tags = TagsCreateSerializer(queryset=models.Tag.objects.all(), many=True)
    ingredients = IngredientsCreateSerializer(many=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Recipe
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        print(ingredients)
        request = self.context['request']
        author = request.user
        recipe = models.Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
        amounts = []
        for ingredient in ingredients:
            instance = ingredient['id']
            obj, status = models.Ingredient.objects.get_or_create(instance)
            print(obj, status)
            amounts.append(obj.id)
        recipe.ingredients.set(amounts)
        # recipe.ingredients.set(ingredients)
        print(author.last_name)
        # author = validated_data.pop('author')
        # print(tags)
        # print(validated_data.pop('tags'))
        # print('asdsadsadsasadadss', validated_data)
        return recipe

    def update(self, instance, validated_data):
        request = self.context['request']
        author = request.user
        if instance.author != author:
            raise PermissionDenied()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.tags.set(tags)
        amounts = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            # TODO проработать TRY EXCEPT ИЛИ get? vmesto get_or_create
            obj, status = models.Ingredient.objects.get_or_create(ingredient_id)
            amounts.append(obj.id)
        instance.ingredients.set(amounts)

        instance.save(update_fields=[
            'image', 'name', 'text', 'cooking_time'
        ])

        print(validated_data)
        print(instance)

        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = models.Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')

    def get_name(self, obj):
        return obj.recipe.name

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.recipe.image.url
        return request.build_absolute_uri(image_url)

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time
