from django.contrib import admin
from .models import Marker, Photo


@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    list_display = ('location', 'date', 'description', 'user')
    list_filter = ('user',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'marker', 'photo')
    list_filter = ('user', 'marker')




