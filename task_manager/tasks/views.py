from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Task
from django.contrib import messages
from task_manager.tasks.forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView,UpdateView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from django.views import View


class TaskIndex(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    def get(self,request):
        tasks = Task.objects.all().order_by('id')
        return render(request,'tasks/tasks_index.html',{'tasks':tasks})

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/tasks_detail.html"
    context_object_name = "task"

class TaskCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_create.html'
    success_message = ("Таска успешно создана!")
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('index_tasks')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = 'next'
    model = Task
    form_class = TaskForm
    template_name = 'tasks/tasks_update.html'
    success_url = reverse_lazy("index_tasks")
    success_message = ("Таска успешно обновлена!")
    login_url = reverse_lazy("login")

    



class TaskDeleteView(LoginRequiredMixin,UserPassesTestMixin, SuccessMessageMixin,DeleteView):
    redirect_field_name = 'next' 
    model = Task
    template_name = "tasks/tasks_delete.html"
    success_url = reverse_lazy("index_tasks")
    success_message = ("Таска успешно удалена!")
    login_url = reverse_lazy("login")
    def test_func(self):
        user_to_delete = self.get_object()
        print(user_to_delete.author) 
        current_user = self.request.user 
        print(current_user)
        return user_to_delete.author == current_user
    def handle_no_permission(self):
        messages.error(self.request, ("Только сам автор может её удалить!"))
        return redirect("index_tasks")