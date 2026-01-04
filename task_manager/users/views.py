from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from task_manager.users.forms import UserFrom,User

def index(request):
    users = User.objects.all()
    return render(request,'users/users_index.html',{'users':users})



class UsersCreateView(View):
    def get(self,request,*args,**kwargs):
        form = UserFrom()
        print(request.user.is_anonymous)
        return render(request,'users/user_create.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form = UserFrom(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['password'] == cleaned_data['temp_pass']:
                form.save()
                print(cleaned_data)
                return redirect('login')

        return render(request,'users/user_create.html',{'form':form})


class UsersUpdateView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request,*args,**kwargs):
        # print(type(request.session.get('_auth_user_id')))
        # print(kwargs['pk'])
        # print(request.user.is_superuser)
        # print(request.session.get('_auth_user_id') == kwargs['pk'])
        if int(request.session.get('_auth_user_id')) == kwargs['pk'] or request.user.is_superuser:
            return render(request,'users/user_update.html')
        return redirect('index_users')
    # Добавить пост запрос и доделать вывод страницы

class UsersDeleteView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request,*args,**kwargs):
        users = User.objects.get(id=kwargs['pk'])
        if int(request.session.get('_auth_user_id')) == kwargs['pk'] or request.user.is_superuser:
            #удалить юзера
            return render(request,'users/user_delete.html',{'user':users})
        return redirect('index_users')



# django.views.generic спросить