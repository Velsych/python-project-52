from django import forms
from .models import Label
from django.core.exceptions import ValidationError
from django.db import models


class LabelFrom(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {'name':'Имя'}