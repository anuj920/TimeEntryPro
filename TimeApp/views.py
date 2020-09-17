from django.shortcuts import redirect, render
from django.views import generic

from  django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from .models import Project, Task
from .forms import ProjectCreateForm, TaskCreateForm
import datetime


class HomeView(generic.TemplateView):
    template_name = 'home.html'


@method_decorator(login_required, name='dispatch')
class ProfileView(generic.TemplateView):
    template_name = 'myprofile.html'



@method_decorator(login_required, name='dispatch')
class ProjectList(generic.ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.filter(user = self.request.user).order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class CreateProjectView(generic.CreateView):
    redirect_field_name = 'project_list.html'
    form_class = ProjectCreateForm
    model = Project

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectDetail(generic.View):

    def get(self,request,**kwargs):
        project_id = kwargs['id']
        project_obj = Project.objects.get(id=project_id)
        task_obj = Task.objects.filter(project=project_obj)
        task_data = []
        l = {}
        for i in task_obj:
            l["task_name"] = i.task_name
            l["created_at"] = i.created_at
            l["start_time"] = datetime.datetime.strptime(i.start_time, "%Y-%m-%dT%H:%M") if i.start_time else 0
            l["end_time"] = datetime.datetime.strptime(i.end_time, "%Y-%m-%dT%H:%M") if i.end_time else 0
            l["working_time"] = (l["end_time"] - l["start_time"]) if(i.start_time and i.end_time) else 0
            task_data.append(l)   
        return render(request,'TimeApp/project_detail.html',{"project_name":project_obj.project_name,"project_created_at":project_obj.created_at,"tasks":task_data})


@method_decorator(login_required, name='dispatch')
class TaskList(generic.View):

    def get(self,request):
        task_obj = Task.objects.filter(project__user=self.request.user).values('id','task_name','created_at','start_time','end_time','is_completed','project__project_name').order_by('is_completed','-created_at')
        # print(task_obj)
        return render(request, 'TimeApp/task_list.html',{"task_list":task_obj})

        

@login_required
def CreateTaskView(request):
    if request.method == 'POST':
        form = TaskCreateForm(request)
        data = request.POST
        pro_obj = Project.objects.get(id=int(data.get("project")))
        Task.objects.create(project=pro_obj,task_name = data.get("task_name"))
        return redirect('task_list')
    else:
        form = TaskCreateForm(request)
    return render(request, 'TimeApp/task_form.html', {'form': form})


@login_required
def UpdateTask(request,id):
    if request.method=='POST':
        data = request.POST
        task_obj = Task.objects.get(id= id)
        task_obj.start_time = data.get("start_time")
        tasks = Task.objects.filter(project__user=request.user).values('id','task_name','created_at','start_time','end_time','is_completed','project__project_name').order_by('is_completed','-created_at')
        s_time = datetime.datetime.strptime(data.get("start_time"), "%Y-%m-%dT%H:%M")
        c_time = datetime.datetime.strptime(task_obj.created_at.strftime("%Y-%m-%dT%H:%M"), "%Y-%m-%dT%H:%M")
        if(s_time<c_time):
            return render(request,'TimeApp/task_list.html',{"error":"Start Time/Date Can't be less than Creation of task time/date","task_list":tasks})
        if(data.get("end_time")):
            e_time = datetime.datetime.strptime(data.get("end_time"), "%Y-%m-%dT%H:%M")
            if(s_time>e_time):
                return render(request,'TimeApp/task_list.html',{"error":"Please Provide a valid Time/Date range","task_list":tasks})
            task_obj.end_time = data.get("end_time")
            task_obj.is_completed = True
        task_obj.save()
        return redirect('task_list')