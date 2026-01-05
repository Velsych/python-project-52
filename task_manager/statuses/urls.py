
from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('', views.index, name='index_statuses'),
    path('create/', views.StatusCreateView.as_view(), name='create_status'),
    # path('<int:pk>/delete/',views.StatusesDeleteView.as_view(),name="delete_status"),
    # path('<int:pk>/update/', views.StatusesUpdateView.as_view(), name='status_update')
]
