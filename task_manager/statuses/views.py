from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Status
from task_manager.statuses.forms import StatusFrom
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView
from django.views import View


class StatusIndex(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    def get(self,request):
        statuses = Status.objects.all()
        return render(request,'statuses/statuses_index.html',{'statuses':statuses})




class StatusCreateView(LoginRequiredMixin,CreateView):
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_statuses')

class StatusUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_update.html'
    success_url = reverse_lazy("index_statuses")
    success_message = ("The user has been successfully updated")
    login_url = reverse_lazy("login")

    



class StatusDeleteView(LoginRequiredMixin, DeleteView):
    redirect_field_name = 'next' 
    model = Status
    template_name = "statuses/statuses_delete.html"
    success_url = reverse_lazy("index_statuses")
    permission_message = ("You do not have permission to delete another user.")
    login_url = reverse_lazy("login")