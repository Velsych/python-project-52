from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from task_manager.users.forms import UserFrom
from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView

def index(request):
    users = User.objects.all()
    return render(request,'users/users_index.html',{'users':users})



class UserPermissionMixin(AccessMixin):
    permission_message = ("You don't have the rights to change another user")
    redirect_url = "index_users"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            return redirect(self.redirect_url)           # redirect_url ?
        return super().dispatch(request, *args, **kwargs)


class UsersCreateView(CreateView):
    model = User
    form_class = UserFrom
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')



class UsersUpdateView(LoginRequiredMixin, UserPermissionMixin,UpdateView):
    redirect_field_name = 'next'
    model = User
    form_class = UserFrom
    template_name = 'users/user_update.html'
    success_url = reverse_lazy("index_users")
    success_message = ("The user has been successfully updated")
    login_url = reverse_lazy("login")
    # Добавить пост запрос и доделать вывод страницы



class UsersDeleteView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("index")
    permission_message = ("You do not have permission to delete another user.")
    login_url = reverse_lazy("login")

# django.views.generic спросить