from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('project_list/',views.ProjectList.as_view(),name="project_list"),
    path('create_project/',views.CreateProjectView.as_view(),name="create_project"),
    path('project_detail/<int:id>/',views.ProjectDetail.as_view(),name="project_detail"),

    path('task_list/',views.TaskList.as_view(),name="task_list"),
    path('create_task/',views.CreateTaskView,name="create_task"),
    path('update_task/<int:id>/',views.UpdateTask,name="update_task"),
    path('profile/',views.ProfileView.as_view(),name='profile')
]