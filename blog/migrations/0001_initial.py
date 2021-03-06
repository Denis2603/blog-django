# Generated by Django 4.0.4 on 2022-06-05 18:05

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')),
                ('text', models.TextField(verbose_name='Текст записи')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Запись блога',
                'verbose_name_plural': 'Записи блога',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='BlogFoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to=blog.models.path_for_foto, verbose_name='Фотография')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foto', to='blog.blog')),
            ],
            options={
                'verbose_name': 'фотография',
                'verbose_name_plural': 'фотографии',
            },
        ),
    ]
