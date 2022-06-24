from django.contrib.auth.models import User
from django.db import models
from pathlib import Path
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def path_for_foto(instance, file_name):
    return Path('blog') / instance.blog.user.username / file_name


class Blog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', verbose_name=_('Автор'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата записи'))
    text = models.TextField(blank=False, verbose_name=_('Текст записи'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('Запись блога')
        verbose_name_plural = _('Записи блога')

    def __str__(self):
        # return f'Автор {self.user.username} ({self.created.strftime("%d %b %Y %H:%M")}). {self.text[:25]}...'
        return _('Автор') + f' {self.user.username} ({self.created.strftime("%d %b %Y %H:%M")}). {self.text[:25]}...'

    def get_absolute_url(self):
        return reverse('detail_blog', args=[self.id])


class BlogFoto(models.Model):

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='foto')
    foto = models.ImageField(blank=False, upload_to=path_for_foto, verbose_name=_('Фотография'))
    description = models.CharField(blank=True, max_length=50, verbose_name=_('Подпись'))

    class Meta:
        verbose_name = _('фотография')
        verbose_name_plural = _('фотографии')

    def __str__(self):
        return _("Фото %(name)s из записи %(blog)s") % {'name': self.foto.name, 'blog': self.blog}

