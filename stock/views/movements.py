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

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to
from django.views.generic import list_detail, create_update
from django.template import RequestContext
from django.contrib import messages

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.products.forms import ProductEntryForm

from ..models import *
from ..forms import *

def _get_movement(request, *args, **kwargs):
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(Movement, id=id)
    return None

@permission_required('stock.change_movement')
def movement_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a movement list.
    """
    return filtered_list_detail(
        request,
        Movement,
        fields=['id', 'origin', 'destination', 'product_entry', 'created'],
        page=page,
        paginate_by=paginate_by,
        template_name='stock/movement_list.html',
        **kwargs
    )

@permission_required('stock.add_movement')     
def movement_add(request, **kwargs):
    """Adds a new movement.
    """
    movement = Movement(author=request.user)  
      
    if request.method == 'POST':
        form = MovementForm(request.POST, instance=movement)
        pform = ProductEntryForm(request.POST)
        if pform.is_valid() and form.is_valid():
            pe = pform.save()
            movement.product_entry = pe
            form.save()
            messages.success(request, _("The movement has been saved."))
            return redirect_to(request, url=movement.get_absolute_url())
    else:
        form = MovementForm(instance=movement)
        pform = ProductEntryForm()

    return render_to_response('stock/movement_edit.html', RequestContext(request, {'form': form, 'pform': pform, 'object': movement}))

@permission_required('stock.change_movement', _get_movement)     
def movement_detail(request, id, page=None, **kwargs):
    """Shows movement details.
    """
    object_list = Movement.objects.all()

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        **kwargs
    )

@permission_required('stock.change_movement', _get_movement)     
def movement_edit(request, id, **kwargs):
    """Edits a movement.
    """
    movement = get_object_or_404(Movement, id=id)  
      
    if request.method == 'POST':
        form = MovementForm(request.POST, instance=movement)
        pform = ProductEntryForm(request.POST, instance=movement.product_entry)
        if pform.is_valid() and form.is_valid():
            pe = pform.save()
            movement.product_entry = pe
            form.save()
            messages.success(request, _("The movement has been saved."))
            return redirect_to(request, url=movement.get_absolute_url())
    else:
        form = MovementForm(instance=movement)
        pform = ProductEntryForm(instance=movement.product_entry)

    return render_to_response('stock/movement_edit.html', RequestContext(request, {'form': form, 'pform': pform, 'object': movement}))

@permission_required('stock.delete_movement', _get_movement)    
def movement_delete(request, id, **kwargs):
    """Deletes a movement.
    """
    return create_update.delete_object(
        request,
        model=Movement,
        object_id=id,
        post_delete_redirect=reverse('movement_list'),
        template_name='stock/movement_delete.html',
        **kwargs
    )
