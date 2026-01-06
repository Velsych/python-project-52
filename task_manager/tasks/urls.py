
from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TaskIndex.as_view(), name='index_tasks'),
    path('create/', views.TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/delete/',views.TaskDeleteView.as_view(),name="delete_task"),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    # path('<int:pk/>',views.TaskDetailView.as_view(),name='detail_task')

]