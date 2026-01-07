import django_filters
from .models import Task,User,Status,Label
from django.forms import CheckboxInput

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=("Статус"),
        empty_label=("Любой статус"),
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=("Исполнитель"),
        empty_label=("Любой исполнитель"),
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=("Метка"),
        empty_label=("Любая метка"),
    )

    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label=("Только мои задачи"),
        widget=CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Task
        fields = ['status','executor','labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        executor_filter = self.filters["executor"]
        executor_filter.field.label_from_instance = User.get_full_name

        # Упорядочиваем queryset для выпадающих списков
        self.filters["status"].queryset = Status.objects.all().order_by("name")
        self.filters["executor"].queryset = User.objects.all().order_by(
            "first_name", "last_name", "username"
        )
        self.filters["labels"].queryset = Label.objects.all().order_by("name")