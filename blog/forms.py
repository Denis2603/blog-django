from django import forms
from django.utils.translation import gettext_lazy as _


class FotoForm(forms.Form):
    files = forms.ImageField(
        required=False,
        label=_('Загрузить фото'),
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )


class FileForm(forms.Form):
    file = forms.FileField(label=_('Загрузить файл'),
                           help_text=_('Выберите файл .csv'))
