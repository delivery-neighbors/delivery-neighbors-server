# Generated by Django 4.0.4 on 2022-09-21 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('neighbor', '0002_alter_userreliability_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category1', models.IntegerField(default=0)),
                ('category2', models.IntegerField(default=0)),
                ('category3', models.IntegerField(default=0)),
                ('category4', models.IntegerField(default=0)),
                ('category5', models.IntegerField(default=0)),
                ('category6', models.IntegerField(default=0)),
                ('category7', models.IntegerField(default=0)),
                ('category8', models.IntegerField(default=0)),
                ('category9', models.IntegerField(default=0)),
                ('category10', models.IntegerField(default=0)),
                ('category11', models.IntegerField(default=0)),
                ('category12', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
