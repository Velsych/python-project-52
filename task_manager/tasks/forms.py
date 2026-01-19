from django import forms
from .models import Task,User,Status,Label
from django.core.exceptions import ValidationError


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].required = False
        self.fields["executor"].queryset = User.objects.all().order_by("first_name", "last_name", "username")
        self.fields["executor"].label_from_instance = User.get_full_name
        self.fields["status"].queryset = Status.objects.all().order_by("id")
        self.fields["labels"].queryset = Label.objects.all().order_by("id")
        self.fields["labels"].required = False


    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {'name':'Имя',
                  'description':'Описание',
                  'status':'Статус',
                  'executor':'Исполнитель',
                  'labels':'Метки'}
        widgets = {"name": forms.TextInput(attrs={"class": "form-control", "placeholder": ("Имя")}),
            "description": forms.Textarea(attrs={"class": "form-control","placeholder": ("Описание"),"rows": 4,}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "executor": forms.Select(attrs={"class": "form-control"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-control"}),}

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise ValidationError(
                ("Длинна таски должна быть больше 2х символов")
            )
        return name