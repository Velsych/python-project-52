from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from task_manager.users.forms import UserForm, UserUpdateForm


class UsersList(ListView):
    model = User
    template_name = 'users/users_index.html'
    

class UsersCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    success_message = ("Пользователь успешно зарегистрирован")
    success_url = reverse_lazy('login')


class UsersUpdateView(LoginRequiredMixin, UserPassesTestMixin,
            SuccessMessageMixin, UpdateView):
    redirect_field_name = 'next'
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy("index_users")
    success_message = ("Пользователь успешно изменен")
    login_url = reverse_lazy("login")

    def test_func(self):
        user = self.get_object() 
        current_user = self.request.user 
        return user == current_user

    def handle_no_permission(self):
        messages.error(self.request, ("У вас нет прав для изменения"))
        return redirect("index_users")
    # Добавить пост запрос и доделать вывод страницы


class UsersDeleteView(LoginRequiredMixin, UserPassesTestMixin,
            SuccessMessageMixin, DeleteView):
    redirect_field_name = 'next' 
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("index_users")
    success_message = ("Пользователь успешно удален")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user.authored_tasks.exists() or user.executioner.exists():
            messages.error(request, "Невозможно удалить пользователя")
            return redirect("index_users")
        return super().post(request, *args, **kwargs)

    def test_func(self):
        user_to_delete = self.get_object() 
        current_user = self.request.user 
        return user_to_delete == current_user

    def handle_no_permission(self):
        messages.error(self.request, ("У вас нет прав для изменения"))
        return redirect("index_users")
    

# django.views.generic спросить