from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm as UserCreationFormClass
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User


class RegisterForm(UserCreationFormClass):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')
