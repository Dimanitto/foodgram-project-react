# Generated by Django 4.1 on 2022-10-11 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_recipe_options_ingredientamount_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
    ]