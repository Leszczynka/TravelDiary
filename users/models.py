from django.db.models import Model
from django.db.models import OneToOneField, TextField, CASCADE
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class UserProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    avatar = ResizedImageField(size=[200, 200], quality=100, default='default.jpg', upload_to='profile_images')
    bio = TextField()