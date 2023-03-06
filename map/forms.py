from django.forms import CharField, ModelForm, ImageField, DateInput, DateField
from .models import Marker, Photo


class AddMarkerForm(ModelForm):
    location = CharField(required=True)
    date = DateField(required=True, widget=DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
    description = CharField(max_length=500, required=False)

    class Meta:
        model = Marker
        fields = ['location', 'date', 'description']


class UpdateMarkerForm(ModelForm):
    class Meta:
        model = Marker
        fields = ['date', 'description']


class AddPhotoForm(ModelForm):
    photo = ImageField(required=False)

    class Meta:
        model = Photo
        fields = ['photo']
