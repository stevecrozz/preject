from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Task(models.Model):
    description = models.TextField(blank=False)
    project = models.ForeignKey(Project)
    assigned_to = models.ForeignKey(User, related_name='assigned_to',
            null=True, blank=True)
    created_by = models.ForeignKey(User, editable=False,
        related_name='task_created_by')
    updated_by = models.ForeignKey(User, editable=False,
        related_name='task_updated_by')
    created_on = models.DateTimeField('date created', auto_now_add=True)
    updated_on = models.DateTimeField('date updated', auto_now=True)

    def __unicode__(self):
        return self.description

