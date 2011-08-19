from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from tasks.models import Task
from tasks.forms import TaskForm

def index(request):
    if 'project_id' in request.GET:
        tasks = Task.objects.filter(project_id=request.GET['project_id'])
    else:
        tasks = Task.objects.all()

    return render_to_response('tasks/index.html', { 'tasks': tasks },
        context_instance=RequestContext(request))

def detail(request, task_id):
    try:
        t = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404

    return render_to_response('tasks/detail.html', { 'task': t },
        context_instance=RequestContext(request))

def claim(request, task_id):
    try:
        t = Task.objects.get(pk=task_id)
        t.assigned_to = request.user
        t.save()
    except Task.DoesNotExist:
        raise Http404

    if 'project_id' in request.GET:
        return HttpResponseRedirect(reverse('project-detail',
            args=request.GET['project_id']))
    else:
        return HttpResponseRedirect(reverse('task-detail', task_id=t.id))

def reject(request, task_id):
    try:
        t = Task.objects.get(pk=task_id)
        t.assigned_to = None
        t.save()
    except Task.DoesNotExist:
        raise Http404

    if 'project_id' in request.GET:
        return HttpResponseRedirect(reverse('project-detail',
            args=request.GET['project_id']))
    else:
        return HttpResponseRedirect(reverse('task-detail', task_id=t.id))

def new(request):
    if request.method == 'POST':
        f = TaskForm(request.POST)
        if f.is_valid():
            task = f.save(commit=False)
            task.created_by = request.user
            task.updated_by = request.user
            task.save()

            if 'project' in request.POST:
                return HttpResponseRedirect(reverse('project-detail',
                    args=request.POST['project']))
            else:
                return HttpResponseRedirect(reverse('task-index'))

    else:
        f = TaskForm()

    return render_to_response('tasks/new.html', { 'form': f },
        context_instance=RequestContext(request))

def edit(request, task_id):
    try:
        p = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        f = TaskForm(request.POST, instance=p)
        if f.is_valid():
            task = f.save(commit=False)
            task.updated_by = request.user
            task.save()
            return HttpResponseRedirect(reverse('task-index'))
    else:
        f = TaskForm(instance=p)

    return render_to_response('tasks/edit.html', { 'form' : f, 'task' : p },
        context_instance=RequestContext(request))
