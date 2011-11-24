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

def _get_faq(request, *args, **kwargs):
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(Faq, id=id)
    return None

@permission_required('knowledge.change_faq')
def faq_list(request, page=0, paginate_by=5, **kwargs):
    """Displays the list of all FAQs.
    """
    return filtered_list_detail(
        request,
        Faq,
        fields=['title', 'question', 'author', 'created'],
        paginate_by=paginate_by,
        page=page,
        **kwargs
    )

@permission_required('knowledge.add_faq')
def faq_add(request, **kwargs):
    """Adds a new FAQ.
    """
    faq = Faq(author=request.user, language=request.user.get_profile().language)

    if request.method == 'POST':
        form = FaqForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, _("The FAQ has been saved."))
            return redirect_to(request, url=faq.get_absolute_url())
    else:
        form = FaqForm(instance=faq)

    return render_to_response('knowledge/faq_edit.html', RequestContext(request, {'form': form, 'object': faq}))

@permission_required('knowledge.change_faq', _get_faq)    
def faq_detail(request, id, **kwargs):
    """Displays the given FAQ.
    """
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=Faq.objects.all(),
        **kwargs
    )

@permission_required('knowledge.change_faq', _get_faq)
def faq_edit(request, id, **kwargs):
    """Edits the given FAQ.
    """
    return create_update.update_object(
        request,
        form_class=FaqForm,
        object_id=id,
        template_name='knowledge/faq_edit.html',
        **kwargs
    )

@permission_required('knowledge.delete_faq', _get_faq)
def faq_delete(request, id, **kwargs):
    """Deletes the given FAQ.
    """
    return create_update.delete_object(
        request,
        model=Faq,
        object_id=id,
        post_delete_redirect=reverse('faq_list'),
        template_name='knowledge/faq_delete.html',
        **kwargs
    )
