from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField


class SignUpForm(UserCreationForm):
    first_name = CharField(max_length=20, required=True)
    last_name = CharField(max_length=20, required=True)
    username = CharField(max_length=20, required=True)
    email = EmailField(max_length=50, required=True)
    password1 = CharField(max_length=50, required=True)
    password2 = CharField(max_length=50, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        self.instance.is_active = True
        return super().save(commit)



