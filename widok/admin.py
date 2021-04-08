from django.contrib import admin
from .models import Obrazek, Kometarz, Oceny

from django.utils.html import format_html


# Register your models here.

@admin.register(Obrazek)
class ObrazekAdmin(admin.ModelAdmin):
    list_display = ['id', 'autor', 'tytul', 'data_publikacji', 'srednia_ocen', 'path']

    def path(self, object):

        if object.obrazek_file:
            return format_html(f'<a href="/media/{object.obrazek_file}" target="_blank">{object.obrazek_file}</a>')
        else:
            return format_html(f'<a href="{object.obrazek_path}" target="_blank">{object.obrazek_path}</a>')


@admin.register(Oceny)
class OcenyAdmin(admin.ModelAdmin):
    list_display = ['id', 'autor', 'obrazek', 'ocena']
    list_filter = ['obrazek']


@admin.register(Kometarz)
class KometarzAdmin(admin.ModelAdmin):
    list_display = ['id', 'autor', 'obrazek', 'tresc']
    list_filter = ['obrazek']
    search_fields = ['tresc']

    actions = ['usun_smieci']

    def usun_smieci(self, request, queryset):
        for q in queryset:
            if len(q.tresc) < 4:
                q.delete()

    usun_smieci.short_description = "Usuwa śmieciowe kometarze"
