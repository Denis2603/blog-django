from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Profile


class ProfileInline(admin.TabularInline):

    model = Profile
    can_delete = False
    readonly_fields = ('preview', )
    fields = ('about', 'ava', 'preview')

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.ava.url}" style="max-height: 200px;">')

    preview.short_description = _('Просмотр фото')


class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'full_name',  'entry_count')
    inlines = (ProfileInline, )

    def full_name(self, user):
        return user.get_full_name()

    def entry_count(self, user):
        return f'{user.blogs.count()}'

    full_name.short_description = _('Полное имя')
    entry_count.short_description = _('Записей в блоге')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
