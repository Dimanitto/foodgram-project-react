import django_filters
from core import models
from django.db.models import Q


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(method='filter_favorite')
    is_in_shopping_cart = django_filters.NumberFilter(method='filter_shopping_cart')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=models.Tag.objects.all()
    )

    class Meta:
        model = models.Recipe
        fields = (
            'is_favorited', 'is_in_shopping_cart', 'author'
        )

    def filter_favorite(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favorites__user=self.request.user)
        elif value == 0:
            return queryset.exclude(favorites__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(shopping_carts__user=self.request.user)
        elif value == 0:
            return queryset.exclude(shopping_carts__user=self.request.user)
        return queryset


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = models.Ingredient
        fields = ('name', )

    def filter_name(self, queryset, name, value):
        """Двойная фильтрация"""
        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        )
