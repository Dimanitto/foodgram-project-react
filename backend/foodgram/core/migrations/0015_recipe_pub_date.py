# Generated by Django 4.1 on 2022-10-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_tag_color_alter_tag_name_alter_tag_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default='2022-10-10', verbose_name='Дата публикации'),
            preserve_default=False,
        ),
    ]
