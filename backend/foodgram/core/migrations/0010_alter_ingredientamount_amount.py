# Generated by Django 4.1 on 2022-10-11 16:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Количество'),
        ),
    ]
