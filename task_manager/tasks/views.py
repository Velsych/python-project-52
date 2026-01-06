from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Task
from task_manager.tasks.forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView
from django.views import View


class TaskIndex(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    def get(self,request):
        tasks = Task.objects.all()
        return render(request,'tasks/tasks_index.html',{'tasks':tasks})




class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_create.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_tasks')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'next'
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_update.html'
    success_url = reverse_lazy("index_tasks")
    success_message = ("The user has been successfully updated")
    login_url = reverse_lazy("login")

    



class TaskDeleteView(LoginRequiredMixin, DeleteView):
    redirect_field_name = 'next' 
    model = Task
    template_name = "tasks/tasks_delete.html"
    success_url = reverse_lazy("index_tasks")
    permission_message = ("You do not have permission to delete another user.")
    login_url = reverse_lazy("login")