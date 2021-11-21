from django.contrib import admin
from django.db import models
from .models import Playlist,PlaylistItem
# Register your models here.

class PlaylistItemInline(admin.TabularInline):
    model=PlaylistItem


class PlaylistAdmin(admin.ModelAdmin):
    inlines=[PlaylistItemInline]
    class Meta:
        model=Playlist

admin.site.register(Playlist)
