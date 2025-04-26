from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price']


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
