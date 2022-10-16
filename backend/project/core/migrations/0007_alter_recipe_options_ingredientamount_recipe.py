# Generated by Django 4.1 on 2022-10-11 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_shoppingcart_unique_shopping_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredientamounts', to='core.recipe'),
            preserve_default=False,
        ),
    ]