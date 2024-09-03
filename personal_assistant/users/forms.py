from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import (
    CharField,
    TextInput,
    EmailInput,
    EmailField,
    PasswordInput,

)


class RegisterForm(UserCreationForm):
    username = CharField(
        max_length=16,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    email = EmailField(
        max_length=50, required=True, widget=EmailInput(attrs={"class": "form-control"})
    )
    password1 = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )
    password2 = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length=16,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    password = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "password")
