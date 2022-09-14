from PIL import Image
from django.contrib.auth.models import User
from django.db.models import TextField, Model, CASCADE, OneToOneField, ImageField, FloatField, CharField, \
    ForeignKey


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


class Location(Model):
    name = CharField(max_length=100, null=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name