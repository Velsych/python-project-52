
from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.index, name='index_users'),
    path('create/', views.UsersCreateView.as_view(), name='create_user'),
    path('<int:pk>/delete/',views.UsersDeleteView.as_view(),name="delete_user"),
    path('<int:pk>/update/', views.UsersUpdateView.as_view(), name='user_update')
]
