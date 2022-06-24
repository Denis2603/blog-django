from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from pathlib import Path


def path_for_avatar(instance, file_name):
    file_name = instance.user.username + Path(file_name).suffix
    path = Path('users') / 'foto' / file_name
    full_path = settings.MEDIA_ROOT / path
    if full_path.is_file():
        full_path.unlink()
    return path


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    about = models.CharField(max_length=500, blank=True, verbose_name=_('О себе'))
    ava = models.ImageField(upload_to=path_for_avatar, default='users/foto/000_no_foto.svg',
                            blank=False, verbose_name=_('Фото'))
