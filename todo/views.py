#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.5'

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from forms import *

def _get_task(request, *args, **kwargs):
    return get_object_or_404(Task, id=kwargs.get('id', None))

@permission_required('todo.view_task') 
def task_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered tasks.
    """
    return filtered_list_detail(
        request,
        Task.objects.planned(user=request.user),
        paginate_by=paginate_by,
        page=page,
        fields=['title', 'start', 'end', 'created', 'closed'],
        **kwargs
    )

@permission_required('todo.view_task') 
def unplanned_task_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered tasks.
    """
    return filtered_list_detail(
        request,
        Task.objects.unplanned(user=request.user),
        paginate_by=paginate_by,
        page=page,
        fields=['title', 'created', 'closed'],
        template_name='todo/unplanned_task_list.html',
        **kwargs
    )

@permission_required('todo.view_task', _get_task)
def task_detail(request, id, **kwargs):
    """Displays a task.
    """
    object_list = Task.objects.filter(user=request.user)
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        template_name='todo/task_detail.html',
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('todo.add_task')    
def task_add(request, **kwargs):
    """Adds a new task.
    """
    task = Task(user=request.user)  
      
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, _("The task has been saved."))
            return redirect_to(request, url=task.get_absolute_url())
    else:
        form = TaskForm(instance=task)

    return render_to_response('todo/task_edit.html', RequestContext(request, {'form': form, 'object': task}))

@permission_required('todo.change_task', _get_task)
def task_edit(request, id, **kwargs):
    """Edits a task.
    """
    task = get_object_or_404(Task, id=id)
        
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, _("The task has been updated."))
            return redirect_to(request, url=task.get_absolute_url())
    else:
        form = TaskForm(instance=task)

    return render_to_response('todo/task_edit.html', RequestContext(request, {'form': form, 'object': task}))

@permission_required('todo.delete_task', _get_task)
def task_delete(request, id, **kwargs):
    """Deletes a task.
    """
    return create_update.delete_object(
            request,
            model=Task,
            object_id=id,
            post_delete_redirect=reverse('task_list'),
            template_name='todo/task_delete.html',
            **kwargs
        )

@permission_required('todo.change_task', _get_task)
def task_close(request, id, **kwargs):
    """Closes an open task.
    """
    task = get_object_or_404(Task, id=id)

    task.closed = datetime.now()
    task.save()
    messages.success(request, _("The task has been closed."))

    return redirect_to(request, permanent=False, url=task.get_absolute_url())

@permission_required('todo.change_task', _get_task)
def task_reopen(request, id, **kwargs):
    """Reopens a closed task.
    """
    task = get_object_or_404(Task, id=id)

    task.closed = None
    task.save()
    messages.success(request, _("The task has been reopened."))

    return redirect_to(request, permanent=False, url=task.get_absolute_url())
