from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import UserForm,UserUpdateForm
from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView,ListView
from django.views.generic.edit import DeleteView


class UsersList(ListView):
    model = User
    template_name = 'users/users_index.html'
    


class UsersCreateView(SuccessMessageMixin,CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    success_message = ("Юзер зарегистрирован")
    success_url = reverse_lazy('login')



class UsersUpdateView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = 'next'
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy("index_users")
    success_message = ("Юзер обновлён")
    login_url = reverse_lazy("login")
    def test_func(self):
        user = self.get_object() 
        current_user = self.request.user 
        return user == current_user
    def handle_no_permission(self):
        messages.error(self.request, ("Только сам юзер может себя изменять!"))
        return redirect("index_users")
    # Добавить пост запрос и доделать вывод страницы



class UsersDeleteView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, DeleteView):
    redirect_field_name = 'next' 
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("index")
    success_message = ("Юзер удалён")
    login_url = reverse_lazy("login")
    def post(self, request, *args, **kwargs):
        user_to_delete  = self.get_object()
        if user_to_delete.authored_tasks.all().exists() or user_to_delete.executioner.all().exists():
            messages.error(self.request, ("На нём есть созданная таска или повешенные"))
            return redirect("index_users")
        else:
            return super().post(self, request, *args, **kwargs)
    def test_func(self):
        user_to_delete = self.get_object() 
        current_user = self.request.user 
        return user_to_delete == current_user
    def handle_no_permission(self):
        messages.error(self.request, ("Только сам юзер может себя удалять!"))
        return redirect("index_users")
    

# django.views.generic спросить