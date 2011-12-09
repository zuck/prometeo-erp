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
from prometeo.documents.models import *
from prometeo.documents.forms import *
from prometeo.documents.views import *

from forms import *

def _get_timesheet(request, *args, **kwargs):
    return get_object_or_404(Timesheet, id=kwargs.get('id', None))

def _get_timesheetentry(request, *args, **kwargs):
    return get_object_or_404(TimesheetEntry, timesheet__id=kwargs.get('timesheet_id', None), id=kwargs.get('id', None))

@permission_required('hr.change_timesheet') 
def timesheet_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered timesheets.
    """
    return filtered_list_detail(
        request,
        Document.objects.get_for_content(Timesheet),
        fields=['code', 'author', 'created', 'owner'],
        paginate_by=paginate_by,
        page=page,
        template_name='hr/timesheet_list.html',
        **kwargs
    )

@permission_required('hr.change_timesheet', _get_timesheet)  
def timesheet_detail(request, id, **kwargs):
    """Displays a timesheet.
    """
    object_list = Document.objects.get_for_content(Timesheet)
    return list_detail.object_detail(
        request,
        object_id=object_list.get(object_id=id).pk,
        queryset=object_list,
        template_name=kwargs.pop('template_name', 'hr/timesheet_detail.html'),
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('hr.add_timesheet')    
def timesheet_add(request, **kwargs):
    """Adds a new timesheet.
    """
    timesheet = Timesheet(date=datetime.now().date())  
    doc = Document(author=request.user, content_object=timesheet)
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = TimesheetForm(request.POST, instance=timesheet)
        formset = TimesheetEntryFormset(request.POST, instance=timesheet)
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            doc.content_object = timesheet 
            dform.save()
            formset.save()
            messages.success(request, _("The timesheet has been saved."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = TimesheetForm(instance=timesheet)
        formset = TimesheetEntryFormset(instance=timesheet)

    return render_to_response('hr/timesheet_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('hr.change_timesheet', _get_timesheet)  
def timesheet_edit(request, id, **kwargs):
    """Edits a timesheet.
    """
    doc = Document.objects.get_for_content(Timesheet).get(object_id=id)
    timesheet = doc.content_object
        
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = TimesheetForm(request.POST, instance=timesheet)
        formset = TimesheetEntryFormset(request.POST, instance=timesheet, queryset=timesheet.entries.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("The timesheet has been updated."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = TimesheetForm(instance=timesheet)
        formset = TimesheetEntryFormset(instance=timesheet, queryset=timesheet.entries.all())

    return render_to_response('hr/timesheet_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': timesheet}))

@permission_required('hr.delete_timesheet', _get_timesheet) 
def timesheet_delete(request, id, **kwargs):
    """Deletes a timesheet.
    """
    return create_update.delete_object(
            request,
            model=Document,
            object_id=Document.objects.get_for_content(Timesheet).get(object_id=id).pk,
            post_delete_redirect=reverse('timesheet_list'),
            template_name='hr/timesheet_delete.html',
            **kwargs
        )

@permission_required('hr.change_timesheet', _get_timesheet)     
def timesheet_hardcopies(request, id, page=0, paginate_by=10, **kwargs):
    """Shows timesheet hard copies.
    """
    return hardcopy_list(request, Document.objects.get_for_content(Timesheet).get(object_id=id).pk, page, paginate_by, **kwargs)

@permission_required('hr.change_timesheet', _get_timesheet)     
def timesheet_add_hardcopy(request, id, **kwargs):
    """Adds an hard copy to the given document.
    """
    return hardcopy_add(request, Document.objects.get_for_content(Timesheet).get(object_id=id).pk, **kwargs)

@permission_required('hr.change_timesheetentry', _get_timesheetentry)
def timesheetentry_delete(request, timesheet_id, id, **kwargs):
    """Deletes a timesheet entry.
    """
    return create_update.delete_object(
            request,
            model=TimesheetEntry,
            object_id=id,
            post_delete_redirect=timesheet.get_absolute_url(),
            template_name='hr/timesheetentry_delete.html',
            **kwargs
        )
