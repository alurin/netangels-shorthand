from django.contrib import admin
from . import models


class ShorthandUrlAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'url', 'views_counter', 'created_at',)

admin.site.register(models.ShorthandUrl, ShorthandUrlAdmin)