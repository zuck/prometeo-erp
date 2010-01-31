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

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.db.models import Q

from prometeo.core.details import ModelDetails

from models import UOM, Category
from forms import UOMForm, CategoryForm
 
def uom_index(request):
    """Show a uom list.
    """
    uoms = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        uoms = UOM.objects.filter(queryset)
    else:
        uoms = UOM.objects.all()
        
    return render_to_response('uoms/index.html', RequestContext(request, {'uoms': uoms}))
     
def uom_add(request):
    """Add a new uom.
    """
    if request.method == 'POST':
        form = UOMForm(request.POST)
        if form.is_valid():
            uom = form.save()
            return redirect_to(request, url='/uoms/view/%s/' % (uom.pk))
    else:
        form = UOMForm()

    return render_to_response('uoms/add.html', RequestContext(request, {'form': form}));
     
def uom_view(request, id):
    """Show uom details.
    """
    uom = get_object_or_404(UOM, pk=id)
    details = ModelDetails(instance=uom)
    return render_to_response('uoms/view.html', RequestContext(request, {'uom': uom, 'details': details}))
     
def uom_edit(request, id):
    """Edit a uom.
    """
    uom = UOM.objects.get(pk=id)
    if request.method == 'POST':
        form = UOMForm(request.POST, instance=uom)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/uoms/view/%s/' % (id))
    else:
        form = UOMForm(instance=uom)
    return render_to_response('uoms/edit.html', RequestContext(request, {'uom': uom, 'form': form}))
    
def uom_delete(request, id):
    """Delete a uom.
    """
    uom = get_object_or_404(UOM, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            uom.delete()
            return redirect_to(request, url='/uoms/');
        return redirect_to(request, url='/uoms/view/%s/' % (id))
    return render_to_response('uoms/delete.html', RequestContext(request, {'uom': uom}))
    
## Categories.
 
def category_index(request):
    """Show a category list.
    """
    categories = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        categories = Category.objects.filter(queryset)
    else:
        categories = Category.objects.all()
        
    return render_to_response('uoms/categories/index.html', RequestContext(request, {'categories': categories}))
     
def category_add(request):
    """Add a new category.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect_to(request, url='/uoms/categories/view/%s/' % (category.pk))
    else:
        form = CategoryForm()

    return render_to_response('uoms/categories/add.html', RequestContext(request, {'form': form}));
     
def category_view(request, id):
    """Show category details.
    """
    category = get_object_or_404(Category, pk=id)
    details = ModelDetails(instance=category)
    return render_to_response('uoms/categories/view.html', RequestContext(request, {'category': category, 'details': details}))
     
def category_edit(request, id):
    """Edit a category.
    """
    category = Category.objects.get(pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/uoms/categories/view/%s/' % (id))
    else:
        form = CategoryForm(instance=category)
    return render_to_response('uoms/categories/edit.html', RequestContext(request, {'category': category, 'form': form}))
    
def category_delete(request, id):
    """Delete a category.
    """
    category = get_object_or_404(Category, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            category.delete()
            return redirect_to(request, url='/uoms/categories/');
        return redirect_to(request, url='/uoms/categories/view/%s/' % (id))
    return render_to_response('uoms/categories/delete.html', RequestContext(request, {'category': category}))
