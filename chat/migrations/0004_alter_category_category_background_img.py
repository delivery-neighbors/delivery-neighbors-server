# Generated by Django 4.0.4 on 2022-08-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_category_category_background_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_background_img',
            field=models.URLField(),
        ),
    ]
