from django import forms
from django.forms import fields
from django.forms.widgets import FileInput
from .models import Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from web import models


class UpdateUser(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('fname', 'lname', 'image','phone','address', 'dob')
        widgets = {
            'image': FileInput(),
        }


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']