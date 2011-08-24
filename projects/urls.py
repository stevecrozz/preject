from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('projects.views',
    url(r'^$', 'index', name='project-index'),
    url(r'^new/$', 'new', name='project-new'),
    url(r'^(?P<project_id>\d+)/$', 'detail', name='project-detail'),
    url(r'^(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/$', 'detail',
        name='project-detail-task'),
    url(r'^(?P<project_id>\d+)/edit/$', 'edit', name='project-edit'),
)
