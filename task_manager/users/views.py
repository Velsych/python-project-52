from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import UserFrom
from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import ProtectedError

def index(request):
    users = User.objects.all()
    return render(request,'users/users_index.html',{'users':users})



class UsersCreateView(CreateView,SuccessMessageMixin):
    model = User
    form_class = UserFrom
    template_name = 'users/user_create.html'
    success_message = ("Юзер зарегистрирован")
    success_url = reverse_lazy('login')



class UsersUpdateView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = 'next'
    model = User
    form_class = UserFrom
    template_name = 'users/user_update.html'
    success_url = reverse_lazy("index_users")
    success_message = ("Юзер обновлён")
    login_url = reverse_lazy("login")
    def test_func(self):
        user_to_delete = self.get_object() 
        current_user = self.request.user 
        return user_to_delete == current_user
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
    # def form_valid(self):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url() 
    #     try:
    #         self.object.delete()
    #         messages.success(self.request, self.success_message)
    #         return redirect(success_url)
    #     except ProtectedError:
    #         messages.error(self.request,"Невозможно удалить пользователя, так как существуют связанные объекты.")
    #         return redirect("index_users")
    def test_func(self):
        user_to_delete = self.get_object() 
        current_user = self.request.user 
        return user_to_delete == current_user
    def handle_no_permission(self):
        messages.error(self.request, ("Только сам юзер может себя удалять!"))
        return redirect("index_users")
    

# django.views.generic спросить