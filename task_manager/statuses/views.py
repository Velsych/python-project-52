from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from task_manager.statuses.forms import StatusFrom

from .models import Status


class StatusIndex(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    model = Status
    template_name = 'statuses/statuses_index.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_statuses')
    success_message = ('Статус успешно создан')
    

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_update.html'
    success_url = reverse_lazy("index_statuses")
    success_message = ("Статус успешно изменен")
    login_url = reverse_lazy("login")


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView): 
    model = Status
    template_name = "statuses/statuses_delete.html"
    success_url = reverse_lazy("index_statuses")
    success_message = ("Статус успешно удален")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        status_to_delete = self.get_object()
        if status_to_delete.status.all().exists():
            messages.error(self.request, ("Невозможно удалить статус"))
            return redirect("index_statuses")
        else:
            return super().post(self, request, *args, **kwargs)