from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import CharField, EmailField, ModelForm, ImageField, FloatField, DateTimeField, SelectDateWidget, \
    DateInput, DateField
from .models import Profile, Location


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=20, required=True)
    last_name = CharField(max_length=20, required=True)
    # username = CharField(max_length=20, required=True)
    email = EmailField(max_length=50, required=True)
    # password1 = CharField(max_length=50, required=True, label='Password')
    # password2 = CharField(max_length=50, required=True, label="Password confirmation")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    # def save(self, commit=True):
    #     self.instance.is_active = True
    #     return super().save(commit)


class EditProfileForm(UserChangeForm):
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=20)
    username = CharField(max_length=20)
    email = EmailField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


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
        model = Profile
        fields = ['avatar', 'bio']


class DateInput(DateInput):
    input_type = 'date'


class AddMarkerForm(ModelForm):
    name = CharField(label='')
    date = DateField(required=False, widget=DateInput())
    description = CharField(max_length=500, required=False)
    photo = ImageField(required=False)
    lat = FloatField(required=False)
    lng = FloatField(required=False)

    class Meta:
        model = Location
        fields = ['name', 'date', 'description', 'photo', 'lat', 'lng']

