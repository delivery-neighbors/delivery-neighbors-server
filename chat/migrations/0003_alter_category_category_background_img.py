# Generated by Django 4.0.4 on 2022-08-07 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_background_img',
            field=models.ImageField(upload_to=''),
        ),
    ]