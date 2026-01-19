from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView

from task_manager.tasks.forms import TaskForm

from .filters import TaskFilter
from .models import Task


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/tasks_index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    ordering = ["-created_at"]

    def get_queryset(self):
        tasks = super().get_queryset()
        return tasks.select_related(
            "status", "author", "executor"
        ).prefetch_related("labels")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/tasks_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, 
        SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_create.html'
    success_message = ("Задача успешно создана")
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    redirect_field_name = 'next'
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_update.html'
    success_url = reverse_lazy("index_tasks")
    success_message = ("Задача успешно изменена")
    login_url = reverse_lazy("login")


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin,
    SuccessMessageMixin, DeleteView):
    redirect_field_name = 'next' 
    model = Task
    template_name = "tasks/tasks_delete.html"
    success_url = reverse_lazy("index_tasks")
    success_message = ("Задача успешно удалена")
    login_url = reverse_lazy("login")

    def test_func(self):
        task_to_delete = self.get_object()
        current_user = self.request.user 
        return task_to_delete.author == current_user

    def handle_no_permission(self):
        messages.error(self.request, ("Задачу может удалить только ее автор"))
        return redirect("index_tasks")