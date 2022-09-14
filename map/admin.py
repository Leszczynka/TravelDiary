from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Profile, LocationMarker

admin.site.register(Profile)


@admin.register(LocationMarker)
class MarkerAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')




