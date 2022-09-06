from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from core import models
from rest_framework.pagination import LimitOffsetPagination

from . import serializers
from .mixins import ListCreateDeleteViewSet
from users.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions, authentication, status, generics
from django_filters.rest_framework import DjangoFilterBackend


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    # TODO не работает поиск по slug пишем свои фильтры?
    filterset_fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags__slug')
    # for ?limit=N
    pagination_class = LimitOffsetPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        # print(dir(self.request))
        # print(self.request.data)
        if self.request.data:
            print('yes!')
            return serializers.RecipeCreateSerializer
        print('no!')
        return serializers.RecipeSerializer


class FavoriteView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

    def post(self, request, id: int):
        author = request.user
        if models.Favorite.objects.filter(user=author, recipe_id=id).exists():
            return Response(
                {
                    'error':
                        (f'Ошибка добавления в избранное. '
                         f'Рецепт "{id}" уже есть в избранном')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite = models.Favorite.objects.create(user=author, recipe_id=id)
        serializer = serializers.FavoriteSerializer(favorite, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id: int):
        author = request.user
        if not models.Favorite.objects.filter(
                user=author, recipe_id=id).exists():
            return Response(
                {
                    'error':
                        (f'Ошибка удаление из избранного. '
                         f'Рецептa "{id}" нету в избранном')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        models.Favorite.objects.filter(
                user=author, recipe_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientListView(generics.ListAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class IngredientDetailView(generics.RetrieveAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    lookup_field = 'id'



