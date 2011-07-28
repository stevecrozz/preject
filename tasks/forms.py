from django.forms import ModelForm
from tasks.models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ('created_on', 'updated_on',)

class MiniTaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ('created_on', 'updated_on', 'assigned_to', 'project',)
