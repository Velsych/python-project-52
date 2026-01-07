from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Label
from task_manager.labels.forms import LabelFrom
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView
from django.views import View


class LabelIndex(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    def get(self,request):
        labels = Label.objects.all().order_by('id')
        return render(request,'labels/labels_index.html',{'labels':labels})




class LabelCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Label
    form_class = LabelFrom
    template_name = 'labels/labels_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_labels')
    success_message = ("Метка успешно добавлена")

class LabelUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = 'next'
    model = Label
    form_class = LabelFrom
    template_name = 'labels/labels_update.html'
    success_url = reverse_lazy("index_labels")
    success_message = ("Метка успешно обновлена")
    login_url = reverse_lazy("login")

    



class LabelDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    redirect_field_name = 'next' 
    model = Label
    template_name = "labels/labels_delete.html"
    success_url = reverse_lazy("index_labels")
    login_url = reverse_lazy("login")
    success_message = ("Метка успешно удалена!")
    def post(self, request, *args, **kwargs):
        label_to_delete  = self.get_object()
        if label_to_delete.label.all().exists():
            messages.error(self.request, ("На нём есть созданная таска!"))
            return redirect("index_labels")
        else:
            return super().post(self, request, *args, **kwargs)