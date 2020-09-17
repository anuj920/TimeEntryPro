from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class CreateModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Project(CreateModel):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    project_name = models.CharField(max_length=128)

    def __str__(self):
        return self.project_name
    
    def get_absolute_url(self):
        return reverse('project_list')


class Task(CreateModel):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=128)
    start_time = models.CharField(blank= True, null=True,max_length=128)
    end_time = models.CharField(blank= True, null=True, max_length=128)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
    
    def get_absolute_url(self):
        return reverse('task_list')