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

@login_required
def widget_add(request, **kwargs):
    """Adds a new widget for the current user's dashboard.
    """
    dashboard = request.user.get_profile().dashboard
    widget = Widget(region=dashboard, sort_order=dashboard.widgets.count())
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=widget)
        if form.is_valid():
            widget.slug = slugify("%s_%s" % (widget.title, request.user.pk))
            widget = form.save()
            messages.success(request, _("The widget has been saved."))
            return redirect_to(request, url="/")
    else:
        form = WidgetForm(instance=widget)

    return render_to_response('widgets/widget_edit.html', RequestContext(request, {'form': form, 'object': widget}))

@login_required
def widget_edit(request, slug, **kwargs):
    """Edits an existing widget for the current user's dashboard.
    """
    dashboard = request.user.get_profile().dashboard
    widget = get_object_or_404(Widget, region=dashboard, slug=slug)

    if request.method == 'POST':
        form = WidgetForm(request.POST, instance=widget)
        if form.is_valid():
            widget = form.save()
            messages.success(request, _("The widget has been updated."))
            return redirect_to(request, url="/")
    else:
        form = WidgetForm(instance=widget)

    return render_to_response('widgets/widget_edit.html', RequestContext(request, {'form': form, 'object': widget}))

@login_required
def widget_delete(request, slug, **kwargs):
    """Deletes an existing widget from the current user's dashboard.
    """
    return create_update.delete_object(
        request,
        model=Widget,
        slug=slug,
        post_delete_redirect='/',
        template_name='widgets/widget_delete.html',
        **kwargs
     )
