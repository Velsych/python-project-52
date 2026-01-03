
from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.index, name='index_users'),
    path('create/', views.UsersCreateView.as_view(), name='create_user'),
    path('update/', views.UsersUpdateView.as_view(), name='user_update')
]
