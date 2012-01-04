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

def _get_warehouse(request, *args, **kwargs):
    warehouse_id = kwargs.get('warehouse_id', None)
    id = kwargs.get('id', None)
    if warehouse_id:
        return get_object_or_404(Warehouse, id=warehouse_id)
    elif id:
        return get_object_or_404(Warehouse, id=id)
    return None

@permission_required('stock.view_warehouse')
def warehouse_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a warehouse list.
    """
    return filtered_list_detail(
        request,
        Warehouse,
        fields=['name', 'owner', 'address'],
        page=page,
        paginate_by=paginate_by,
        template_name='stock/warehouse_list.html',
        **kwargs
    )

@permission_required('stock.add_warehouse')     
def warehouse_add(request, **kwargs):
    """Adds a new warehouse.
    """
    warehouse = Warehouse(author=request.user)  
      
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request, _("The warehouse was created successfully."))
            return redirect_to(request, url=warehouse.get_absolute_url())
    else:
        form = WarehouseForm(instance=warehouse)

    return render_to_response('stock/warehouse_edit.html', RequestContext(request, {'form': form, 'object': warehouse}))

@permission_required('stock.view_warehouse', _get_warehouse)     
def warehouse_detail(request, id, page=None, **kwargs):
    """Shows warehouse details.
    """
    object_list = Warehouse.objects.all()

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        **kwargs
    )

@permission_required('stock.change_warehouse', _get_warehouse)     
def warehouse_edit(request, id, **kwargs):
    """Edits a warehouse.
    """
    return create_update.update_object(
        request,
        object_id=id,
        form_class=WarehouseForm,
        template_name='stock/warehouse_edit.html'
    )

@permission_required('stock.delete_warehouse', _get_warehouse)    
def warehouse_delete(request, id, **kwargs):
    """Deletes a warehouse.
    """
    return create_update.delete_object(
        request,
        model=Warehouse,
        object_id=id,
        post_delete_redirect=reverse('warehouse_list'),
        template_name='stock/warehouse_delete.html',
        **kwargs
    )

@permission_required('stock.view_warehouse', _get_warehouse) 
def warehouse_movements(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the warehouse's movements.
    """
    warehouse = get_object_or_404(Warehouse, pk=id)

    return filtered_list_detail(
        request,
        Movement.objects.for_warehouse(warehouse),
        fields=['id', 'origin', 'destination', 'product_entry', 'created'],
        page=page,
        paginate_by=paginate_by,
        template_name='stock/warehouse_movements.html',
        extra_context={'object': warehouse},
        **kwargs
    )

@permission_required('stock.change_warehouse', _get_warehouse)
@permission_required('stock.add_movement')
def warehouse_add_ingoing_movement(request, id, **kwargs):
    """Adds a new movement to the given warehouse.
    """
    movement = Movement(destination_id=id, author=request.user)

    if request.method == 'POST':
        form = IngoingMovementForm(request.POST, instance=movement)
        pform = ProductEntryForm(request.POST)
        if pform.is_valid() and form.is_valid():
            pe = pform.save()
            movement.product_entry = pe
            form.save()
            messages.success(request, _("The movement was created successfully."))
            return redirect_to(request, url=movement.get_absolute_url())
    else:
        form = IngoingMovementForm(instance=movement)
        pform = ProductEntryForm()

    return render_to_response('stock/warehouse_edit_movement.html', RequestContext(request, {'form': form, 'pform': pform, 'object': movement}))

@permission_required('stock.change_warehouse', _get_warehouse)
@permission_required('stock.add_movement')
def warehouse_add_outgoing_movement(request, id, **kwargs):
    """Adds a new movement from the given warehouse.
    """
    movement = Movement(origin_id=id, author=request.user)

    if request.method == 'POST':
        form = OutgoingMovementForm(request.POST, instance=movement)
        pform = ProductEntryForm(request.POST)
        if pform.is_valid() and form.is_valid():
            pe = pform.save()
            movement.product_entry = pe
            form.save()
            messages.success(request, _("The movement was created successfully."))
            return redirect_to(request, url=movement.get_absolute_url())
    else:
        form = OutgoingMovementForm(instance=movement)
        pform = ProductEntryForm()

    return render_to_response('stock/warehouse_edit_movement.html', RequestContext(request, {'form': form, 'pform': pform, 'object': movement}))
