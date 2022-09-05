from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db.models import PointField
from django.db.models import CharField, TextField, DateField, Model, OneToOneField, CASCADE


class Marker(models.Model):
    name = CharField(max_length=100)
    location = PointField(srid=4326)
    description = TextField()
    date = DateField(null=True)
