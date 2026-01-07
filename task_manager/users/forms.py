from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserFrom(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.'
    )
    
    temp_pass = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Подтверждение пароля',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля необязательными при редактировании
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['temp_pass'].required = False

    def clean_password(self):
        password1 = self.cleaned_data.get("password")
        if self.instance.pk and not password1:
            return password1

        if len(password1) < 3:
            raise ValidationError(
                ("Password must be at least 3 characters long")
            )
        return password1

    def clean_temp_pass(self):
        password = self.cleaned_data.get("password")
        temp_pass = self.cleaned_data.get("temp_pass")
        if self.instance.pk and not password and not temp_pass:
            return temp_pass
        if password != temp_pass:
            raise ValidationError(("The entered passwords do not match."))
        return temp_pass
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if self.instance.pk and not password:
            current_user = User.objects.get(pk=self.instance.pk)
            user.password = current_user.password
        else:
            user.set_password(password)

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
        'password': 'Пароль'
    }
        help_texts = {
        'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        'password': 'Ваш пароль должен содержать как минимум 3 символа.'
    }