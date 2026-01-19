from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from task_manager.forms import LogInForm
from django.contrib.auth import authenticate, login,logout

def index(request):
    return render(request,'index.html')

def user_logout(request):
    logout(request)
    messages.success(request, ("Вы разлогинены"))
    return redirect('index')



class LogIn(View):
    def get(self,request,*args,**kwargs):
        form = LogInForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("Вы залогинены"))
            return redirect('index')
        else:
            messages.error(
                request, ("ПОправь пароль")
            )
            return render(request,'index.html')