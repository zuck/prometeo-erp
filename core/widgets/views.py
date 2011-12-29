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
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib import messages

from prometeo.core.utils import clean_referer
from prometeo.core.auth.decorators import obj_permission_required as permission_required

from models import *
from forms import *

def _get_region(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    return get_object_or_404(Region, slug=slug)

def _get_widget(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    return get_object_or_404(Widget, slug=slug)

@permission_required('widgets.add_widget')
@permission_required('widgets.change_region', _get_region)
def widget_add(request, slug, **kwargs):
    """Adds a new widget to the given region.
    """
    next = request.GET.get('next', clean_referer(request))

    region = get_object_or_404(Region, slug=slug)
    widget = Widget(region=region, sort_order=region.widgets.count(), editable=True)

    if request.method == 'POST':
        form = WidgetForm(request.POST, instance=widget)
        if form.is_valid():
            widget.slug = slugify("%s_%s" % (widget.title, request.user.pk))
            widget = form.save()
            messages.success(request, _("The widget has been saved."))
            return redirect_to(request, url=next)
    else:
        form = WidgetForm(instance=widget)

    return render_to_response('widgets/widget_edit.html', RequestContext(request, {'form': form, 'object': widget, 'next': next}))

@permission_required('widgets.change_widget', _get_widget)
def widget_edit(request, slug, **kwargs):
    """Edits an existing widget.
    """
    next = request.GET.get('next', clean_referer(request))

    widget = get_object_or_404(Widget, slug=slug)

    if request.method == 'POST':
        form = WidgetForm(request.POST, instance=widget)
        if form.is_valid():
            widget = form.save()
            messages.success(request, _("The widget has been updated."))
            return redirect_to(request, url=next)
    else:
        form = WidgetForm(instance=widget)

    return render_to_response('widgets/widget_edit.html', RequestContext(request, {'form': form, 'object': widget, 'next': next}))

@permission_required('widgets.delete_widget', _get_widget)
def widget_delete(request, slug, **kwargs):
    """Deletes an existing widget.
    """
    next = request.GET.get('next', clean_referer(request))

    return create_update.delete_object(
        request,
        model=Widget,
        slug=slug,
        post_delete_redirect=next,
        template_name='widgets/widget_delete.html',
        extra_context={'next': next},
        **kwargs
     )
