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
__version__ = '0.0.2'

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.conf import settings

from prometeo.core.utils import filter_objects

from forms import *

@permission_required('todo.change_task') 
def task_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered tasks.
    """
    object_list = Task.objects.planned(user=request.user)

    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Task,
                                                fields=['title', 'start', 'end', 'created', 'closed'],
                                                object_list=object_list
                                              )

    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        **kwargs
    )

@permission_required('todo.change_task') 
def unplanned_task_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered tasks.
    """
    object_list = Task.objects.unplanned(user=request.user)

    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Task,
                                                fields=['title', 'created', 'closed'],
                                                object_list=object_list
                                              )

    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        template_name='todo/unplanned_task_list.html',
        extra_context={
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        **kwargs
    )
  
def task_detail(request, id, **kwargs):
    """Displays a task.
    """
    task = get_object_or_404(Task, pk=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_task') or request.user == task.user)):
        messages.error(request, _("You can't view this task."))
        return redirect_to(request, url=reverse('user_login'))

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
  
def task_edit(request, id, **kwargs):
    """Edits a task.
    """
    task = get_object_or_404(Task, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_task') or request.user == task.user)):
        messages.error(request, _("You can't edit this task."))
        return redirect_to(request, url=reverse('user_login'))
        
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, _("The task has been updated."))
            return redirect_to(request, url=task.get_absolute_url())
    else:
        form = TaskForm(instance=task)

    return render_to_response('todo/task_edit.html', RequestContext(request, {'form': form, 'object': task}))
  
def task_delete(request, id, **kwargs):
    """Deletes a task.
    """ 
    task = get_object_or_404(Task, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.delete_task') or request.user == task.user)):
        messages.error(request, _("You can't delete this task."))
        return redirect_to(request, url=task.get_absolute_url())

    return create_update.delete_object(
            request,
            model=Task,
            object_id=id,
            post_delete_redirect='/tasks/',
            template_name='todo/task_delete.html',
            **kwargs
        )

def task_close(request, id, **kwargs):
    """Closes an open task.
    """
    task = get_object_or_404(Task, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_task') or request.user == task.user)):
        messages.error(request, _("You can't close this task."))
        return redirect_to(request, url=task.get_absolute_url())

    task.closed = datetime.now()
    task.save()
    messages.success(request, _("The task has been closed."))

    return redirect_to(request, permanent=False, url=task.get_absolute_url())

def task_reopen(request, id, **kwargs):
    """Reopens a closed task.
    """
    task = get_object_or_404(Task, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_task') or request.user == task.user)):
        messages.error(request, _("You can't reopen this task."))
        return redirect_to(request, url=task.get_absolute_url())

    task.closed = None
    task.save()
    messages.success(request, _("The task has been reopened."))

    return redirect_to(request, permanent=False, url=task.get_absolute_url())
