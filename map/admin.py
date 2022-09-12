from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Profile, Marker

admin.site.register(Profile)


@admin.register(Marker)
class MarkerAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')



