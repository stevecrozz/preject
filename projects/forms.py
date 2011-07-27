from django.forms import ModelForm
from projects.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('created_on', 'updated_on',)
