# Generated by Django 4.0.4 on 2022-08-07 18:16

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='https://deliveryneighborsbucket.s3.ap-northeast-2.amazonaws.com/media/avatar/default_img.jpg', storage=storages.backends.s3boto3.S3Boto3Storage, upload_to=''),
        ),
    ]
