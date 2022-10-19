# Generated by Django 4.1 on 2022-09-04 14:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_recipe_is_favorited_recipe_is_in_shopping_cart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='core.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Количество',
                'verbose_name_plural': 'Количество',
            },
        ),
    ]