from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField, ModelForm, ImageField, FloatField, DateInput, DateField
from .models import UserProfile, Marker


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    username = CharField(max_length=50, required=True)
    email = EmailField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(ModelForm):
    avatar = ImageField()
    bio = CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']


class AddMarkerForm(ModelForm):
    location = CharField(label='')
    date = DateField(required=False)
    description = CharField(max_length=500, required=False)
    photo = ImageField(required=False)
    lat = FloatField(required=False)
    lng = FloatField(required=False)

    class Meta:
        model = Marker
        fields = ['location', 'date', 'description', 'photo', 'lat', 'lng']
