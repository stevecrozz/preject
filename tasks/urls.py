from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tasks.views',
    url(r'^$', 'index', name='task-index'),
    url(r'^new/$', 'new', name='task-new'),
    url(r'^(?P<task_id>\d+)/$', 'detail', name='task-detail'),
    url(r'^(?P<task_id>\d+)/edit/$', 'edit', name='task-edit'),
    url(r'^(?P<task_id>\d+)/claim/$', 'claim', name='task-claim'),
    url(r'^(?P<task_id>\d+)/reject/$', 'reject', name='task-reject'),
)
