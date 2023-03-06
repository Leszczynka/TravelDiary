from django.db.models import Model
from django.db.models import OneToOneField, ImageField, TextField, CASCADE
from django.contrib.auth.models import User
from PIL import Image


class UserProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    avatar = ImageField(default='default.jpg', upload_to='profile_images')
    bio = TextField()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
        if img.height > 400 or img.width > 400:
            new_img = (400, 400)
            img.thumbnail(new_img)
            img.save(self.avatar.path)