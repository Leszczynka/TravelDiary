from PIL import Image
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models import TextField, Model, CASCADE, OneToOneField, ImageField, FloatField, CharField, \
    ForeignKey, DateField

from traveldiary import settings


class UserProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    avatar = CloudinaryField('image')
    bio = TextField()


class Marker(Model):
    location = CharField(max_length=100, null=False)
    date = DateField(null=True, blank=True)
    description = TextField(max_length=500, blank=True, null=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.location


class Photo(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    marker = ForeignKey(Marker, on_delete=CASCADE)
    photo = CloudinaryField('image', blank=True, null=True)

    def get_photo_url(self):
        return '{}{}'.format(settings.CLOUDINARY_ROOT_URL, self.photo)

