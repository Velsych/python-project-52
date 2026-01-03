from django import forms
from django.contrib.auth.models import User


class UserFrom(forms.ModelForm):
    temp_pass = forms.CharField()
    temp_pass.help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
    temp_pass.label = 'Подтверждение пароля'
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        labels = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'username': 'Имя пользователя',
        'password': 'Пароль'
    }
        help_texts = {
        'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        'password': 'Ваш пароль должен содержать как минимум 3 символа.'
    }