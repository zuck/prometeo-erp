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

from prometeo.core.utils import filter_objects

from ..models import *
from ..forms import *

@permission_required('projects.change_project') 
def project_list(request, page=0, paginate_by=5, **kwargs):
    """Displays the list of all published projects.
    """
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Project,
                                                fields=['id', 'title', 'author', 'manager', 'created', 'status'],
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
    
@permission_required('projects.change_project') 
def project_detail(request, slug, **kwargs):
    """Displays the selected project.
    """
    object_list = Project.objects.all()
    return list_detail.object_detail(
        request,
        slug=slug,
        queryset=object_list,
        **kwargs
    )

@permission_required('projects.add_project')     
def project_add(request, **kwargs):
    """Adds a new project.
    """
    project = Project(author=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, _("The project has been saved."))
            return redirect_to(request, url=project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)

    return render_to_response('projects/project_edit.html', RequestContext(request, {'form': form, 'object': project}))

@permission_required('projects.change_project')     
def project_edit(request, slug, **kwargs):
    """Edits a project.
    """
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, _("The project has been saved."))
            return redirect_to(request, url=project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)

    return render_to_response('projects/project_edit.html', RequestContext(request, {'form': form, 'object': project}))

@permission_required('projects.delete_project')     
def project_delete(request, slug, **kwargs):
    """Deletes a project.
    """ 
    project = get_object_or_404(Project, slug=slug)
    return create_update.delete_object(
            request,
            model=Project,
            slug=slug,
            post_delete_redirect='/projects/',
            template_name='projects/project_delete.html',
            **kwargs
        )
