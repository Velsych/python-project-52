from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.users.forms import UserFrom

def index(request):
    return render(request,'users/users_index.html')

class UsersCreateView(View):
    def get(self,request,*args,**kwargs):
        form = UserFrom()
        print(request.user.is_anonymous)
        return render(request,'users/user_create.html',{'form':form})
    def post(self,request,*args,**kwargs):
        pass


class UsersUpdateView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request,*args,**kwargs):
        print(request.user.is_anonymous)
        return render(request,'users/user_update.html')