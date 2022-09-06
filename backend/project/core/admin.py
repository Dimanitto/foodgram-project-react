from django.contrib import admin
from core import models


@admin.register(models.Ingredient)
class Ingredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(models.Recipe)
class Recipe(admin.ModelAdmin):
    list_display = ('name', 'author', 'count')
    list_filter = ('author', 'name', 'tags')

    @admin.display(empty_value='0', description='Кол-во добавлений в избранное')
    def count(self, obj):
        print(obj.name)
        # return self.is_favorited.count
        # TODO Favorite table and users FIX IT! (Favorite.objects.filter(recipe_is_favorited=True).filter(recipe_name=obj.name)
        return models.Favorite.objects.filter(recipe__is_favorited=True).filter(recipe__name=obj.name).count()
    # TODO На странице рецепта вывести общее число добавлений этого рецепта в избранное.


@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
