from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField
from .models import Profile
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

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=50,
                             required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email']
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

