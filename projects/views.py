from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from projects.models import Project
from projects.forms import ProjectForm

def index(request):
    projects = Project.objects.all()
    return render_to_response('projects/index.html', {
        'projects': projects,
    }, context_instance=RequestContext(request))

def detail(request, project_id):
    try:
        p = Project.objects.get(pk=project_id)
        tasks = p.task_set.all()
    except Project.DoesNotExist:
        raise Http404

    return render_to_response('projects/detail.html', {
        'project': p,
        'tasks': tasks,
    }, context_instance=RequestContext(request))

def new(request):
    if request.method == 'POST':
        f = ProjectForm(request.POST)
        if f.is_valid():
            project = f.save(commit=False)
            project.created_by = request.user
            project.updated_by = request.user
            project.save()
            return HttpResponseRedirect(reverse('project-index'))
    else:
        f = ProjectForm()

    return render_to_response('projects/new.html', { 'form': f },
        context_instance=RequestContext(request))

def edit(request, project_id):
    try:
        p = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        f = ProjectForm(request.POST, instance=p)
        if f.is_valid():
            project = f.save(commit=False)
            project.updated_by = request.user
            project.save()
            return HttpResponseRedirect(reverse('project-index'))
    else:
        f = ProjectForm(instance=p)

    return render_to_response('projects/edit.html', { 'form' : f, 'project' : p },
        context_instance=RequestContext(request))
