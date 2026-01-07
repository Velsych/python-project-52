from django import forms
from .models import Label


class LabelFrom(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {'name':'Имя'}