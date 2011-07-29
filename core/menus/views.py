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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib import messages

from prometeo.core.filter import filter_objects

from models import *
from forms import *

def clean_referer(request):
    try:
        referer = request.META['HTTP_REFERER']
    except:
        referer = '/'
    return referer.replace("http://", "").replace(request.META['HTTP_HOST'], "")

@login_required
def bookmark_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all bookmarks for the current user.
    """
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Link,
                                                fields=['title', 'url'],
                                                object_list=request.user.get_profile().bookmarks.links.all()
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
        template_name='menus/bookmark_list.html',
        **kwargs
    )

@login_required
def bookmark_add(request, **kwargs):
    """Adds a new bookmark for the current user.
    """
    bookmarks = request.user.get_profile().bookmarks
    link = Link(menu=bookmarks, sort_order=bookmarks.links.count())
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            link.slug = slugify("%s_%s" % (link.title, request.user.pk))
            link = form.save()
            messages.success(request, _("The link has been saved."))
            return redirect_to(request, url="/")
    else:
        url = clean_referer(request)
        if url == reverse('bookmark_list', args=[]):
            url = ""
        link.url = url
        form = LinkForm(instance=link)

    return render_to_response('menus/bookmark_edit.html', RequestContext(request, {'form': form, 'object': link}))

@login_required
def bookmark_edit(request, slug, **kwargs):
    """Edits an existing bookmark for the current user.
    """
    bookmarks = request.user.get_profile().bookmarks
    link = get_object_or_404(Link, menu=bookmarks, slug=slug)

    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            link = form.save()
            messages.success(request, _("The link has been updated."))
            return redirect_to(request, url="/")
    else:
        form = LinkForm(instance=link)

    return render_to_response('menus/bookmark_edit.html', RequestContext(request, {'form': form, 'object': link}))

@login_required
def bookmark_delete(request, slug, **kwargs):
    """Deletes an existing bookmark for the current user.
    """
    return create_update.delete_object(
        request,
        model=Link,
        slug=slug,
        post_delete_redirect='/',
        template_name='menus/bookmark_delete.html',
        **kwargs
     )
