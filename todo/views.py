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

from prometeo.core.views import filtered_list_detail

from forms import *

@permission_required('todo.change_task') 
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

@permission_required('todo.change_task') 
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
        return redirect_to(request, url=reverse('user_login'))

    return create_update.delete_object(
            request,
            model=Task,
            object_id=id,
            post_delete_redirect=reverse('task_list'),
            template_name='todo/task_delete.html',
            **kwargs
        )

def task_close(request, id, **kwargs):
    """Closes an open task.
    """
    task = get_object_or_404(Task, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_task') or request.user == task.user)):
        messages.error(request, _("You can't close this task."))
        return redirect_to(request, url=reverse('user_login'))

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
        return redirect_to(request, url=reverse('user_login'))

    task.closed = None
    task.save()
    messages.success(request, _("The task has been reopened."))

    return redirect_to(request, permanent=False, url=task.get_absolute_url())

@permission_required('todo.change_timesheet') 
def timesheet_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered timesheets.
    """
    return filtered_list_detail(
        request,
        Timesheet.objects.filter(user=request.user),
        paginate_by=paginate_by,
        page=page,
        fields=['date', 'status', 'created'],
        **kwargs
    )
  
def timesheet_detail(request, id, **kwargs):
    """Displays a timesheet.
    """
    timesheet = get_object_or_404(Timesheet, pk=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_timesheet') or request.user == timesheet.user)):
        messages.error(request, _("You can't view this timesheet."))
        return redirect_to(request, url=reverse('user_login'))

    object_list = Timesheet.objects.filter(user=request.user)

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        template_name='todo/timesheet_detail.html',
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('todo.add_timesheet')    
def timesheet_add(request, **kwargs):
    """Adds a new timesheet.
    """
    timesheet = Timesheet(user=request.user, date=datetime.now().date())  
      
    if request.method == 'POST':
        form = TimesheetForm(request.POST, instance=timesheet)
        formset = TimesheetEntryFormset(request.POST, instance=timesheet)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("The timesheet has been saved."))
            return redirect_to(request, url=timesheet.get_absolute_url())
    else:
        form = TimesheetForm(instance=timesheet)
        formset = TimesheetEntryFormset(instance=timesheet)

    return render_to_response('todo/timesheet_edit.html', RequestContext(request, {'form': form, 'formset': formset, 'object': timesheet}))
  
def timesheet_edit(request, id, **kwargs):
    """Edits a timesheet.
    """
    timesheet = get_object_or_404(Timesheet, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.change_timesheet') or request.user == timesheet.user)):
        messages.error(request, _("You can't edit this timesheet."))
        return redirect_to(request, url=reverse('user_login'))
        
    if request.method == 'POST':
        form = TimesheetForm(request.POST, instance=timesheet)
        formset = TimesheetEntryFormset(request.POST, instance=timesheet, queryset=timesheet.entries.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("The timesheet has been updated."))
            return redirect_to(request, url=timesheet.get_absolute_url())
    else:
        form = TimesheetForm(instance=timesheet)
        formset = TimesheetEntryFormset(instance=timesheet, queryset=timesheet.entries.all())

    return render_to_response('todo/timesheet_edit.html', RequestContext(request, {'form': form, 'formset': formset, 'object': timesheet}))
  
def timesheet_delete(request, id, **kwargs):
    """Deletes a timesheet.
    """ 
    timesheet = get_object_or_404(Timesheet, id=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.delete_timesheet') or request.user == timesheet.user)):
        messages.error(request, _("You can't delete this timesheet."))
        return redirect_to(request, url=reverse('user_login'))

    return create_update.delete_object(
            request,
            model=Timesheet,
            object_id=id,
            post_delete_redirect=reverse('timesheet_list'),
            template_name='todo/timesheet_delete.html',
            **kwargs
        )

def timesheetentry_delete(request, timesheet_id, id, **kwargs):
    """Deletes a timesheet entry.
    """
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)
    entry = get_object_or_404(TimesheetEntry, id=id, timesheet=timesheet)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('todo.delete_timesheetentry') or request.user == entry.timesheet.user)):
        messages.error(request, _("You can't delete this timesheet entry."))
        return redirect_to(request, url=reverse('user_login'))

    return create_update.delete_object(
            request,
            model=TimesheetEntry,
            object_id=id,
            post_delete_redirect=timesheet.get_absolute_url(),
            template_name='todo/timesheetentry_delete.html',
            **kwargs
        )
