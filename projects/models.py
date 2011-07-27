from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField('date created', auto_now_add=True)
    updated_on = models.DateTimeField('date updated', auto_now=True)

    def __unicode__(self):
        return self.name

