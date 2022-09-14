from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField, ModelForm, ImageField
from .models import Profile, Location
from django import forms


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=20, required=True)
    last_name = CharField(max_length=20, required=True)
    username = CharField(max_length=20, required=True)
    email = EmailField(max_length=50, required=True)
    password1 = CharField(max_length=50, required=True, label='Password')
    password2 = CharField(max_length=50, required=True, label="Password confirmation")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        self.instance.is_active = True
        return super().save(commit)


class UpdateUserForm(ModelForm):
    username = CharField(max_length=50, required=True)
    email = EmailField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = ImageField()
    bio = CharField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class SearchForm(forms.ModelForm):
    address = forms.CharField(label='')


    class Meta:
        model = Location
        fields = ['address', ]
        exclude = ['user']
