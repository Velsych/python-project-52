from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



class UserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "password1",'password2']
        labels = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'username': 'Имя пользователя',
        'password1': 'Пароль',
        'password2': 'Подтверждение пароля'
    }
        help_texts = {
        'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        'password1': 'Ваш пароль должен содержать как минимум 3 символа.',
        'password2': 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
    }


class UserUpdateForm(UserForm):
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
                username
                and self._meta.model.objects.filter(
            username__iexact=username
        ).exists()
                and self.instance.username != username
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username