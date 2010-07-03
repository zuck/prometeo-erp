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

__author__ = 'Emanuele Bertoldi <zuck@fastwebnet.it>'
__copyright__ = 'Copyright (c) 2010 Emanuele Bertoldi'
__version__ = '$Revision$'

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.db.models import Q

from prometeo.core.details import ModelDetails, ModelPaginatedListDetails
from prometeo.core.paginator import paginate

from models import *
from forms import *
from details import *

@permission_required('warehouses.change_warehouse')
def warehouse_index(request):
    """Show a warehouse list.
    """
    warehouses = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        warehouses = Warehouse.objects.filter(queryset)
    else:
        warehouses = Warehouse.objects.all()
        
    warehouses = WarehouseListDetails(request, warehouses)
        
    return render_to_response('warehouses/index.html', RequestContext(request, {'warehouses': warehouses}))

@permission_required('warehouses.add_warehouse') 
def warehouse_add(request):
    """Add a new warehouse.
    """
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save()
            return redirect_to(request, url='/warehouses/view/%s/' % (warehouse.pk))
    else:
        form = WarehouseForm()

    return render_to_response('warehouses/add.html', RequestContext(request, {'form': form}));

@permission_required('warehouses.change_warehouse')     
def warehouse_view(request, id, page=None):
    """Show warehouse details.
    """
    warehouse = get_object_or_404(Warehouse, pk=id)
    
    # Movements.
    if page == 'movements':
        movements = MovementListDetails(request, warehouse.movement_set.all(), exclude=['id', 'warehouse_id', 'account_id', 'payment_delay'])
        return render_to_response('warehouses/movements.html', RequestContext(request, {'warehouse': warehouse, 'movements': movements}))
        
    
    # Details.
    details = ModelDetails(instance=warehouse)
    details.add_field(_('value'), '%.2f' % warehouse.value())
    return render_to_response('warehouses/view.html', RequestContext(request, {'warehouse': warehouse, 'details': details}))

@permission_required('warehouses.change_warehouse')
def warehouse_edit(request, id):
    """Edit a warehouse.
    """
    warehouse = Warehouse.objects.get(pk=id)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/warehouses/view/%s/' % (id))
    else:
        form = WarehouseForm(instance=warehouse)
    return render_to_response('warehouses/edit.html', RequestContext(request, {'warehouse': warehouse, 'form': form}))

@permission_required('warehouses.delete_warehouse')    
def warehouse_delete(request, id):
    """Delete a warehouse.
    """
    warehouse = get_object_or_404(Warehouse, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            warehouse.delete()
            return redirect_to(request, url='/warehouses/');
        return redirect_to(request, url='/warehouses/view/%s/' % (id))
    return render_to_response('warehouses/delete.html', RequestContext(request, {'warehouse': warehouse}))

@permission_required('warehouses.change_movement')     
def movement_index(request):
    """Show a movement list.
    """
    movements = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        movements = Movement.objects.filter(queryset)
    else:
        movements = Movement.objects.all()
        
    movements = MovementListDetails(request, movements, exclude=['id', 'account_id', 'payment_delay'])
        
    return render_to_response('warehouses/movements/index.html', RequestContext(request, {'movements': movements}))

@permission_required('warehouses.add_movement')     
def movement_add(request, warehouse_id):
    """Add a new movement.
    """
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    movement = Movement(warehouse=warehouse)
    wizard = MovementWizard(initial=movement, template="warehouses/movements/add.html")
    wizard.extra_context['movement'] = movement
    return wizard(request)

@permission_required('warehouses.change_movement')     
def movement_view(request, warehouse_id, id):
    """Show movement details.
    """
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    movement = get_object_or_404(Movement, pk=id)
    if movement.warehouse != warehouse:
        raise Http404
    
    details = ModelDetails(instance=movement)
    details.add_field(_('value'), movement.value())
    
    return render_to_response('warehouses/movements/view.html', RequestContext(request, {'movement': movement, 'details': details}))

@permission_required('warehouses.change_movement')     
def movement_edit(request, warehouse_id, id):
    """Edit a movement.
    """
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    movement = get_object_or_404(Movement, pk=id)
    if movement.warehouse != warehouse:
        raise Http404
    
    wizard = MovementWizard(initial=movement, template="warehouses/movements/edit.html")
    wizard.extra_context['movement'] = movement
    return wizard(request)

@permission_required('warehouses.delete_movement')    
def movement_delete(request, warehouse_id, id):
    """Delete a movement.
    """
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    movement = get_object_or_404(Movement, pk=id)
    if movement.warehouse != warehouse:
        raise Http404
    
    if not movement.is_last():
        referer_view = get_referer_view(request, movement.warehouse.get_absolute_url())
        return HttpResponseRedirect(referer_view)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            warehouse = movement.warehouse
            movement.delete()
            return redirect_to(request, url=warehouse.get_absolute_url());
        return redirect_to(request, url='/warehouses/movements/view/%s/' % (id))
    return render_to_response('warehouses/movements/delete.html', RequestContext(request, {'movement': movement}))
    
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 Arthur Furlan <arthur.furlan@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# On Debian systems, you can find the full text of the license in
# /usr/share/common-licenses/GPL-2

import re

def get_referer_view(request, default=None):
    ''' 
    Return the referer view of the current request

    Example:

        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    if referer[0] != request.META.get('SERVER_NAME'):
        return default

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer

