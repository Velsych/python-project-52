from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserFrom(forms.ModelForm):
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
        # Делаем поля необязательными при редактировании
        if self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        if self.instance.pk and not password1:
            return password1

        if len(password1) < 3:
            raise ValidationError(
                ("Password must be at least 3 characters long")
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if self.instance.pk and not password1 and not password2:
            return password2
        if password1 != password2:
            raise ValidationError(("The entered passwords do not match."))
        return password2
    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if self.instance.pk and not password1:
            current_user = User.objects.get(pk=self.instance.pk)
            user.password1 = current_user.password1
        else:
            user.set_password(password1)

        if commit:
            user.save()
        return user
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        labels = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'username': 'Имя пользователя',
        'password1': 'Пароль'
    }
        help_texts = {
        'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        'password': 'Ваш пароль должен содержать как минимум 3 символа.'
    }