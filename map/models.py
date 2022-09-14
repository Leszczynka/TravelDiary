from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db.models import CharField, TextField, DateField, Model, CASCADE, OneToOneField, ImageField, EmailField, \
    ForeignKey
from django.db import models
from django.conf import settings


class LocationMarker(Model):
    name = CharField(max_length=100)
    location = PointField(srid=4326)
    description = TextField()
    date = DateField(null=True)


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    avatar = ImageField(default='default.jpg', upload_to='profile_images')
    bio = TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Location(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.address

