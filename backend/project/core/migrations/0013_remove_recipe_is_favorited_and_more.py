# Generated by Django 4.1 on 2022-10-15 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_ingredient_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='is_favorited',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='is_in_shopping_cart',
        ),
    ]
