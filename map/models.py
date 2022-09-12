from PIL import Image
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db.models import TextField, Model, CASCADE, OneToOneField, ImageField, FloatField, DateField, CharField


class Marker(Model):
    name = CharField(max_length=100, null=True)
    location = PointField(null=True)


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    avatar = ImageField(default='default.jpg', upload_to='profile_images')
    bio = TextField()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


