from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField, ModelForm, ImageField, DateInput, DateField
from .models import UserProfile, Marker, Photo


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
