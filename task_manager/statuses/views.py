from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Status
from django.contrib import messages
from task_manager.statuses.forms import StatusFrom
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,UpdateView,ListView
from django.views.generic.edit import DeleteView
from django.views import View


class StatusIndex(LoginRequiredMixin,ListView):
    login_url = reverse_lazy("login")
    model = Status
    template_name = 'statuses/statuses_index.html'
    context_object_name = 'statuses'




class StatusCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_statuses')
    success_message = ('Статус успешно создан')
    
class StatusUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_update.html'
    success_url = reverse_lazy("index_statuses")
    success_message = ("Статус успешно обновлён")
    login_url = reverse_lazy("login")

    



class StatusDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView): 
    model = Status
    template_name = "statuses/statuses_delete.html"
    success_url = reverse_lazy("index_statuses")
    success_message = ("Статус успешно удалён")
    login_url = reverse_lazy("login")
    def post(self, request, *args, **kwargs):
        status_to_delete  = self.get_object()
        if status_to_delete.status.all().exists():
            messages.error(self.request, ("На нём есть созданная таска!"))
            return redirect("index_statuses")
        else:
            return super().post(self, request, *args, **kwargs)