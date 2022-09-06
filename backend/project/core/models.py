from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=255)
    count = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество должно быть > 0'
            )
        ]
    )
    measurement_unit = models.CharField('Единица измерения', max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField('Название', max_length=255)
    color = models.CharField('Цветовой HEX-код', max_length=255)
    slug = models.CharField('Slug', max_length=255)

    def __str__(self) -> str:
        return f'{self.name} {self.color}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    # TODO "is_favorited": true, "is_in_shopping_cart": true, Связная таблица для них
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    is_favorited = models.BooleanField('В избранном', default=False)
    is_in_shopping_cart = models.BooleanField('В списке покупок', default=False)
    name = models.CharField('Назввание', max_length=255)
    image = models.ImageField('Картинка', upload_to='recipes/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipe_ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipe_tags'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления должно быть > 0'
            )
        ]
    )

    def __str__(self) -> str:
        return f'{self.author} - {self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return f'{self.user}, {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self) -> str:
        return f'{self.user}, {self.recipe.name}'


class IngredientAmount(models.Model):
    amount = models.FloatField(
        'Количество',
        validators=[MinValueValidator(0.01)]
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientamounts',
        verbose_name='Ингредиент'
    )

    class Meta:
        verbose_name = 'Количество'
        verbose_name_plural = 'Количество'

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'
