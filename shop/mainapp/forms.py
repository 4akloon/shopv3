from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import *


class ReviewForm(forms.ModelForm):
    text = forms.CharField()

    class Meta:
        model = Reviews
        fields = ('text',)


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True, label='Имя')
    last_name = forms.CharField(max_length=50, required=True, label='Фамилия')

    def get_user(self):
        return self.user_cache

    class Meta:
        model = User
        fields = ("username", "email", "first_name", 'last_name')
        field_classes = {'username': UsernameField}


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('address', 'comment',)
