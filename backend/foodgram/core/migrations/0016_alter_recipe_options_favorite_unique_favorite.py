# Generated by Django 4.1 on 2022-10-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_recipe_pub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]