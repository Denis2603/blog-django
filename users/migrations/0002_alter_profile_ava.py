# Generated by Django 4.0.4 on 2022-06-06 07:37

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ava',
            field=models.ImageField(default='users/foto/000_no_foto.svg', upload_to=users.models.path_for_avatar, verbose_name='Фото'),
        ),
    ]