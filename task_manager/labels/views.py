from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Label
from task_manager.labels.forms import LabelFrom
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,UpdateView,ListView
from django.views.generic.edit import DeleteView


class LabelIndex(LoginRequiredMixin,ListView):
    login_url = reverse_lazy("login")
    model = Label
    template_name = 'labels/labels_index.html'
    context_object_name = 'labels'




class LabelCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Label
    form_class = LabelFrom
    template_name = 'labels/labels_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_labels')
    success_message = ("Метка успешно создана")

class LabelUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = 'next'
    model = Label
    form_class = LabelFrom
    template_name = 'labels/labels_update.html'
    success_url = reverse_lazy("index_labels")
    success_message = ("Метка успешно изменена")
    login_url = reverse_lazy("login")

    



class LabelDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    redirect_field_name = 'next' 
    model = Label
    template_name = "labels/labels_delete.html"
    success_url = reverse_lazy("index_labels")
    login_url = reverse_lazy("login")
    success_message = ("Метка успешно удалена")
    def post(self, request, *args, **kwargs):
        label_to_delete  = self.get_object()
        if label_to_delete.label.all().exists():
            messages.error(self.request, ("Невозможно удалить метку"))
            return redirect("index_labels")
        else:
            return super().post(self, request, *args, **kwargs)