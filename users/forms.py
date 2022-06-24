from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserChangeFormCustom(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'email': 'e-mail'}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about']
        widgets = {'about': forms.Textarea(attrs={'cols': 60, 'rows': 4})}
