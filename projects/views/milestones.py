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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from prometeo.core.filter import filter_objects

from ..models import *
from ..forms import *

@permission_required('projects.change_milestone') 
def milestone_list(request, project, page=0, paginate_by=5, **kwargs):
    """Displays the list of all milestones of a specified project.
    """
    project = get_object_or_404(Project, slug=project)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Milestone,
                                                fields=['id', 'title', 'parent', 'author', 'manager', 'created', 'date_due', 'closed'],
                                                object_list=project.milestones.all(),
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'project': project,
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        **kwargs
    )
 
@permission_required('projects.change_milestone')    
def milestone_detail(request, project, slug, **kwargs):
    """Show milestone details.
    """
    project = get_object_or_404(Project, slug=project)
    object_list = project.milestone_set.all()
    return list_detail.object_detail(
        request,
        slug=slug,
        queryset=object_list,
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('projects.add_milestone')    
def milestone_add(request, project, **kwargs):
    """Adds a new milestone.
    """
    project = get_object_or_404(Project, slug=project)
    milestone = Milestone(project=project, author=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            messages.success(request, _("The milestone has been saved."))
            return redirect_to(request, url=milestone.get_absolute_url())
    else:
        form = MilestoneForm(instance=milestone)

    return render_to_response('projects/milestone_edit.html', RequestContext(request, {'form': form, 'object': milestone}))

@permission_required('projects.change_milestone')    
def milestone_edit(request, project, slug, **kwargs):
    """Edits a milestone.
    """
    project = get_object_or_404(Project, slug=project)
    milestone = get_object_or_404(Milestone, project=project, slug=slug)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            messages.success(request, _("The milestone has been saved."))
            return redirect_to(request, url=milestone.get_absolute_url())
    else:
        form = MilestoneForm(instance=milestone)

    return render_to_response('projects/milestone_edit.html', RequestContext(request, {'form': form, 'object': milestone}))

@permission_required('projects.delete_milestone')     
def milestone_delete(request, project, slug, **kwargs):
    """Deletes a milestone.
    """ 
    project = get_object_or_404(Project, slug=project)
    return create_update.delete_object(
            request,
            model=Milestone,
            slug=slug,
            post_delete_redirect='/projects/%s/milestones' % project.slug,
            template_name='projects/milestone_delete.html',
            **kwargs
        )

@permission_required('projects.change_milestone')
@permission_required('projects.change_ticket')  
def milestone_tickets(request, project, slug, page=0, paginate_by=5, **kwargs):
    """Displays the list of all tickets of a specified milestone.
    """
    project = get_object_or_404(Project, slug=project)
    milestone = get_object_or_404(Milestone, slug=slug)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Ticket,
                                                fields=['id', 'title', 'parent', 'author', 'manager', 'created', 'closed', 'urgency', 'status'],
                                                object_list=milestone.tickets.all(),
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'project': project,
            'field_names': field_names,
            'filter_fields': filter_fields,
            'object': milestone
        },
        template_name='projects/milestone_tickets.html',
        **kwargs
    )
