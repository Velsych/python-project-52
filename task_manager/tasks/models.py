from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT,related_name='status')
    executor = models.ForeignKey(User, on_delete=models.PROTECT,blank=True,null=True, related_name='executioner') 
    labels = models.ManyToManyField(Label,related_name='label',blank=True)
    author = models.ForeignKey(User,on_delete=models.PROTECT,related_name="authored_tasks")
    created_at = models.DateTimeField(auto_now_add=True)