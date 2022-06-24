# Generated by Django 4.0.4 on 2022-06-05 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(blank=True, max_length=500, verbose_name='О себе')),
                ('ava', models.ImageField(blank=True, default='users/foto/000_no_foto.svg', upload_to=users.models.path_for_avatar, verbose_name='Фото')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
