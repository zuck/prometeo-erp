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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.contrib import messages

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from ..models import *
from ..forms import *

def _get_milestone(request, *args, **kwargs):
    project_code = kwargs.get('project', None)
    milestone_code = kwargs.get('code', None)
    return get_object_or_404(Milestone, code=milestone_code, project__code=project_code)

@permission_required('projects.view_milestone') 
def milestone_list(request, project, page=0, paginate_by=5, **kwargs):
    """Displays the list of all milestones of a specified project.
    """
    project = get_object_or_404(Project, code=project)
    return filtered_list_detail(
        request,
        project.milestone_set.all(),
        fields=['code', 'title', 'parent', 'author', 'manager', 'created', 'deadline', 'closed'],
        paginate_by=paginate_by,
        page=page,
        extra_context={'object': project},
        **kwargs
    )
 
@permission_required('projects.view_milestone', _get_milestone)    
def milestone_detail(request, project, code, **kwargs):
    """Show milestone details.
    """
    project = get_object_or_404(Project, code=project)
    milestone = get_object_or_404(Milestone, code=code)
    object_list = project.milestone_set.all()
    return list_detail.object_detail(
        request,
        object_id=milestone.pk,
        queryset=object_list,
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('projects.add_milestone')    
def milestone_add(request, project, **kwargs):
    """Adds a new milestone.
    """
    project = get_object_or_404(Project, code=project)
    milestone = Milestone(project=project, author=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            messages.success(request, _("The milestone was created successfully."))
            return redirect_to(request, url=milestone.get_absolute_url())
    else:
        form = MilestoneForm(instance=milestone)

    return render_to_response('projects/milestone_edit.html', RequestContext(request, {'form': form, 'object': milestone}))

@permission_required('projects.change_milestone', _get_milestone)    
def milestone_edit(request, project, code, **kwargs):
    """Edits a milestone.
    """
    project = get_object_or_404(Project, code=project)
    milestone = get_object_or_404(Milestone, project=project, code=code)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            messages.success(request, _("The milestone was updated successfully."))
            return redirect_to(request, url=milestone.get_absolute_url())
    else:
        form = MilestoneForm(instance=milestone)

    return render_to_response('projects/milestone_edit.html', RequestContext(request, {'form': form, 'object': milestone}))

@permission_required('projects.delete_milestone', _get_milestone)     
def milestone_delete(request, project, code, **kwargs):
    """Deletes a milestone.
    """ 
    project = get_object_or_404(Project, code=project)
    milestone = get_object_or_404(Milestone, project=project, code=code)
    return create_update.delete_object(
        request,
        model=Milestone,
        object_id=milestone.pk,
        post_delete_redirect='/projects/%s/milestones' % project.code,
        template_name='projects/milestone_delete.html',
        **kwargs
    )

@permission_required('projects.change_milestone', _get_milestone)
def milestone_close(request, project, code, **kwargs):
    """Closes an open milestone.
    """
    project = get_object_or_404(Project, code=project)
    milestone = get_object_or_404(Milestone, code=code)

    milestone.closed = datetime.datetime.now()
    milestone.save()
    messages.success(request, _("The milestone has been closed."))

    return redirect_to(request, permanent=False, url=milestone.get_absolute_url())

@permission_required('projects.change_milestone', _get_milestone)
def milestone_reopen(request, project, code, **kwargs):
    """Reopens a closed milestone.
    """
    project = get_object_or_404(Project, code=project)
    milestone = get_object_or_404(Milestone, code=code)

    milestone.closed = None
    milestone.save()
    messages.success(request, _("The milestone has been reopened."))

    return redirect_to(request, permanent=False, url=milestone.get_absolute_url())

@permission_required('projects.view_milestone', _get_milestone)
@permission_required('projects.view_ticket')  
def milestone_tickets(request, project, code, page=0, paginate_by=5, **kwargs):
    """Displays the list of all tickets of a specified milestone.
    """
    project = get_object_or_404(Project, code=project)
    milestone = get_object_or_404(Milestone, code=code)
    return filtered_list_detail(
        request,
        milestone.tickets.all(),
        fields=['id', 'title', 'parent', 'author', 'manager', 'created', 'closed', 'urgency', 'status'],
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'project': project,
            'object': milestone
        },
        template_name='projects/milestone_tickets.html',
        **kwargs
    )
