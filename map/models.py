from PIL import Image
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db.models import CharField, TextField, DateField, Model, CASCADE, OneToOneField, ImageField, EmailField


class Marker(Model):
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
