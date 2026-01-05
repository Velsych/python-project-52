from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Status
from task_manager.statuses.forms import StatusFrom
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView

def index(request):
    statuses = Status.objects.all()
    return render(request,'statuses/statuses_index.html',{'statuses':statuses})




class StatusCreateView(LoginRequiredMixin,CreateView):
    model = Status
    form_class = StatusFrom
    template_name = 'statuses/statuses_create.html'
    success_url = reverse_lazy('index_statuses')