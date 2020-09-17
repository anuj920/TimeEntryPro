from django import forms
from .models import Project, Task


class ProjectCreateForm(forms.ModelForm):

    class Meta():
        model = Project
        fields = ('project_name',)

        widgets = {
            'project_name': forms.TextInput(attrs = {'class': 'textinputclass'}),
        }

class TaskCreateForm(forms.ModelForm):

    class Meta():
        model = Task
        fields = ('task_name','project')

    def __init__(self,request,*args,**kwargs):
        super (TaskCreateForm,self ).__init__(*args,**kwargs)
        self.fields['project'].queryset = Project.objects.filter(user = request.user)