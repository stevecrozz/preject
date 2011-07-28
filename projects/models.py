from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, editable=False,
        related_name='created_by')
    updated_by = models.ForeignKey(User, editable=False,
        related_name='updated_by')
    created_on = models.DateTimeField('date created', auto_now_add=True)
    updated_on = models.DateTimeField('date updated', auto_now=True)

    def __unicode__(self):
        return self.name

