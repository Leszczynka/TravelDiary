from django.contrib.gis import admin
from .models import UserProfile, Marker, Photo

admin.site.register(UserProfile)
admin.site.register(Marker)
admin.site.register(Photo)





