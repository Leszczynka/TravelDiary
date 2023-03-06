from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm, ImageField, EmailField
from .models import UserProfile


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