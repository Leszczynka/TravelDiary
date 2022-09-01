from django.db import models
from django.contrib.gis.db.models import PointField
from django.db.models import CharField, TextField, DateField


class Marker(models.Model):
    name = CharField(max_length=100)
    location = PointField()
    description = TextField()
    date = DateField(null=True)
