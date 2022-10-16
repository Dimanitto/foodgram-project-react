from rest_framework import serializers
from .models import User, Subscriber
from core import models
from api.serializers import ImageDecode
from django.contrib.auth import authenticate
from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    """Переопределим базовый класс для дополнительного поля"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj) -> bool:
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            return False
        return user.is_subscriber(obj)


class CustomCreateTokenSerializerTwo(serializers.ModelSerializer):
    default_error_messages = {
        "invalid_credentials": 'Не верные данные!',
    }

    class Meta:
        model = User
        fields = ('password', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get('email')
        params = {'email': attrs.get('email')}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        self.user = User.objects.filter(email=email).first()
        if self.user and self.user.check_password(password):
            return attrs
        self.fail('invalid_credentials')


class SubscriberSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscriber
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_email(self, obj):
        return obj.author.email

    def get_id(self, obj):
        return obj.author.id

    def get_username(self, obj):
        return obj.author.username

    def get_first_name(self, obj):
        return obj.author.first_name

    def get_last_name(self, obj):
        return obj.author.last_name

    def get_is_subscribed(self, obj):
        return obj.user.is_subscriber(obj.author)

    def get_recipes(self, obj):
        recipes_limit = self.context.get('recipes_limit')
        recipes = obj.author.recipes.all()[:recipes_limit]
        return RecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj) -> int:
        return obj.author.recipes.count()


class RecipeSerializer(serializers.ModelSerializer):
    image = ImageDecode()

    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
