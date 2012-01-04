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

from django.http import Http404
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

def _get_page(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    try:
        return get_object_or_404(WikiPage, slug=slug)
    except:
        return None

@permission_required('knowledge.view_wikipage')
def page_list(request, page=0, paginate_by=5, **kwargs):
    """Displays the list of all wiki pages.
    """
    return filtered_list_detail(
        request,
        WikiPage,
        fields=['slug', 'language', 'author', 'created'],
        paginate_by=paginate_by,
        page=page,
        **kwargs
    )

@permission_required('knowledge.view_wikipage', _get_page)        
def page_detail(request, slug, **kwargs):
    """Displays the selected page.
    """
    # The page already exists.
    try:
        return list_detail.object_detail(
            request,
            slug=slug,
            queryset=WikiPage.objects.all(),
            **kwargs
        )
        
    # The page needs to be created.
    except Http404:
        return render_to_response("knowledge/wikipage_404.html", RequestContext(request, {'slug': slug}));

@permission_required('knowledge.change_wikipage', _get_page)
def page_edit(request, slug=None, **kwargs):
    """Edits or creates a page.
    """
    try:
        page = WikiPage.objects.get(slug=slug)
    except WikiPage.DoesNotExist:
        page = WikiPage(slug=slug, author=request.user, language=request.user.get_profile().language)

    if request.method == 'POST':
        form = WikiPageForm(request.POST, instance=page)
        if form.is_valid():
            is_new = (not page.pk)
            form.save()
            if is_new:
                messages.success(request, _("The page was created successfully."))
            else:
                messages.success(request, _("The page was updated successfully."))
            return redirect_to(request, url=page.get_absolute_url())
    else:
        form = WikiPageForm(instance=page)

    return render_to_response('knowledge/wikipage_edit.html', RequestContext(request, {'form': form, 'object': page}))

@permission_required('knowledge.view_wikipage', _get_page)        
def page_revisions(request, slug, page=0, paginate_by=10, **kwargs):
    """Displays the list of revisions for the selected page.
    """
    object = get_object_or_404(WikiPage, slug=slug)
    return filtered_list_detail(
        request,
        object.revisions.all(),
        fields=['slug', 'body', 'author', 'created'],
        paginate_by=paginate_by,
        page=page,
        template_name='knowledge/wikipage_revisions.html',
        extra_context={'object': object},
        **kwargs
    )

@permission_required('knowledge.view_wikipage', _get_page)    
def page_revision_detail(request, slug, created, **kwargs):
    """Displays the revision details.
    """
    object = get_object_or_404(WikiRevision, page__slug=slug, created=created)
    return render_to_response('knowledge/wikipage_revision_detail.html', RequestContext(request, {'object': object}))
        
@permission_required('knowledge.delete_wikipage', _get_page)
def page_delete(request, slug, **kwargs):
    """Deletes a page.
    """
    return create_update.delete_object(
            request,
            model=WikiPage,
            slug=slug,
            post_delete_redirect=reverse('wikipage_detail', args=[slug]),
            template_name='knowledge/wikipage_delete.html',
            **kwargs
        )
        
