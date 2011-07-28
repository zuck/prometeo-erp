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

@permission_required('projects.change_area') 
def area_list(request, project, page=0, paginate_by=5, **kwargs):
    """Displays the list of all areas of a specified project.
    """
    project = get_object_or_404(Project, slug=project)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Area,
                                                fields=['id', 'title', 'parent', 'author', 'manager', 'created'],
                                                object_list=project.areas.all(),
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
 
@permission_required('projects.change_area')    
def area_detail(request, project, slug, **kwargs):
    """Show area details.
    """
    project = get_object_or_404(Project, slug=project)
    object_list = project.area_set.all()
    return list_detail.object_detail(
        request,
        slug=slug,
        queryset=object_list,
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('projects.add_area')    
def area_add(request, project, **kwargs):
    """Adds a new area.
    """
    project = get_object_or_404(Project, slug=project)
    area = Area(project=project, author=request.user)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            area = form.save()
            messages.success(request, _("The area has been saved."))
            return redirect_to(request, url=area.get_absolute_url())
    else:
        form = AreaForm(instance=area)

    return render_to_response('projects/area_edit.html', RequestContext(request, {'form': form, 'object': area}))

@permission_required('projects.change_area')    
def area_edit(request, project, slug, **kwargs):
    """Edits an area.
    """
    project = get_object_or_404(Project, slug=project)
    area = get_object_or_404(Area, project=project, slug=slug)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            area = form.save()
            messages.success(request, _("The area has been saved."))
            return redirect_to(request, url=area.get_absolute_url())
    else:
        form = AreaForm(instance=area)

    return render_to_response('projects/area_edit.html', RequestContext(request, {'form': form, 'object': area}))

@permission_required('projects.delete_area')     
def area_delete(request, project, slug, **kwargs):
    """Deletes an area.
    """ 
    project = get_object_or_404(Project, slug=project)
    return create_update.delete_object(
            request,
            model=Area,
            slug=slug,
            post_delete_redirect='/projects/%s/areas' % project.slug,
            template_name='projects/area_delete.html',
            **kwargs
        )

@permission_required('projects.change_area')
@permission_required('projects.change_ticket')  
def area_tickets(request, project, slug, page=0, paginate_by=5, **kwargs):
    """Displays the list of all tickets of a specified area.
    """
    project = get_object_or_404(Project, slug=project)
    area = get_object_or_404(Area, slug=slug)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Ticket,
                                                fields=['id', 'title', 'parent', 'author', 'manager', 'created', 'date_due', 'closed'],
                                                object_list=area.ticket_set.all(),
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
            'object': area
        },
        **kwargs
    )
