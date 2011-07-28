from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^projects/', include('projects.urls')),
    (r'^tasks/', include('tasks.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
