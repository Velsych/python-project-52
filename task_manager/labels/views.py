from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Label
from task_manager.labels.forms import LabelFrom
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView
from django.views import View


class LabelIndex(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    def get(self,request):
        labels = Label.objects.all()
        return render(request,'labels/labels_index.html',{'labels':labels})




class LabelCreateView(LoginRequiredMixin,CreateView):
    model = Label
    form_class = LabelFrom
    template_name = 'labels/labels_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_labels')

class LabelUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    model = Label
    form_class = LabelFrom
    template_name = 'labels/labels_update.html'
    success_url = reverse_lazy("index_labels")
    success_message = ("The user has been successfully updated")
    login_url = reverse_lazy("login")

    



class LabelDeleteView(LoginRequiredMixin, DeleteView):
    redirect_field_name = 'next' 
    model = Label
    template_name = "labels/labels_delete.html"
    success_url = reverse_lazy("index_labels")
    permission_message = ("You do not have permission to delete another user.")
    login_url = reverse_lazy("login")