from django import forms
from .models import Status
from django.core.exceptions import ValidationError
from django.db import models


class StatusFrom(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name':'Название'}