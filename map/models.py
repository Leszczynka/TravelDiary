from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db.models import PointField
from django.db.models import CharField, TextField, DateField, Model,CASCADE


class Marker(models.Model):
    name = CharField(max_length=100)
    location = PointField(srid=4326)
    description = TextField()
    date = DateField(null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username