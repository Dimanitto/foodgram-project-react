from django.contrib import admin
from core import models


@admin.register(models.Ingredient)
class Ingredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class IngredientInline(admin.TabularInline):
    model = models.Recipe.ingredients.through
    extra = 0


@admin.register(models.Recipe)
class Recipe(admin.ModelAdmin):
    inlines = (IngredientInline, )
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('count',)

    @admin.display(empty_value='0', description='Кол-во добавлений в избранное')
    def count(self, obj):
        return models.Favorite.objects.filter(recipe__name=obj.name).count()


@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
