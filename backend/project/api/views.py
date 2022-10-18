from django.core.exceptions import ValidationError, PermissionDenied
from core import models
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Sum
from rest_framework.decorators import action
from .datatools.reports import ReportCsv
from .filters import RecipeFilter, IngredientFilter
from .pagination import CustomPagination

from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
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
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        # Для неавторизованного пользователя
        if self.action == 'list' or self.action == 'retrieve':
            return []
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request) -> HttpResponse:
        user = request.user
        qs = models.ShoppingCart.objects.filter(user=user)
        if not qs:
            raise ValidationError('Нет записей списка покупок')
        columns = [
            'Название', 'Количество', 'Единица измерения'
        ]
        qs = qs.values(
            'recipe__ingredientamounts__ingredient__name',
            'recipe__ingredientamounts__ingredient__measurement_unit'
        ).annotate(sum=Sum('recipe__ingredientamounts__amount'))

        response = ReportCsv(qs, columns, user.first_name).get_http_response()
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return serializers.RecipeCreateSerializer
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class IngredientDetailView(generics.RetrieveAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    lookup_field = 'id'


class ShoppingCartView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FavoriteSerializer

    def post(self, request, id: int):
        user = request.user
        try:
            favorite = models.ShoppingCart.objects.create(user=user, recipe_id=id)
            serializer = serializers.FavoriteSerializer(favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {'error': 'Ошибка добавления в список покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id: int):
        user = request.user
        if not models.ShoppingCart.objects.filter(
                user=user, recipe_id=id).exists():
            return Response(
                {
                    'error':
                        (f'Ошибка удаление из списка покупок. '
                         f'Рецептa "{id}" нету в списке покупок')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        models.ShoppingCart.objects.filter(
            user=user, recipe_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
