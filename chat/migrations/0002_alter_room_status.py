# Generated by Django 4.0.4 on 2022-07-27 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(default='JOINED', max_length=10),
        ),
    ]