from django import forms
from django.contrib.auth.models import User


class LogInForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ["username", "password"]
        labels = {
        'username': 'Имя пользователя',
        'password': 'Пароль'
    }
        help_texts = {
        'username': '',
        'password': ''
    }