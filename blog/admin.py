from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Blog, BlogFoto
from django.utils.translation import gettext_lazy as _


class FotoInline(admin.TabularInline):
    model = BlogFoto
    readonly_fields = ('preview',)
    fields = ('foto', 'preview', 'description', )
    extra = 1

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 150px;">')

    preview.short_description = _('Просмотр')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    date_hierarchy = 'created'
    list_filter = ('user',)
    search_fields = ['text']
    inlines = [FotoInline, ]


@admin.register(BlogFoto)
class BlogFotoAdmin(admin.ModelAdmin):

    list_filter = ('blog', )
    readonly_fields = ('preview',)
    fields = ('blog', 'foto', 'description', 'preview')

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.foto.url}" style="max-height: 200px;">')

    preview.short_description = _('Просмотр')
