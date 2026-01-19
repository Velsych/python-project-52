from django import forms

from .models import Status


class StatusFrom(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': 'Имя'}