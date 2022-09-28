from PIL import Image
from django.contrib.auth.models import User
from django.db.models import TextField, Model, CASCADE, OneToOneField, ImageField, FloatField, CharField, \
    ForeignKey, DateField


class UserProfile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    avatar = ImageField(default='default.jpg', upload_to='profile_images')
    bio = TextField()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Marker(Model):
    location = CharField(max_length=100, null=True)
    date = DateField(blank=True, null=True)
    description = TextField(max_length=500, blank=True, null=True)
    photo = ImageField(blank=True, null=True, upload_to='travel_images')
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.location

    def save(self, *args, **kwargs):
        super().save()
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.photo.path)