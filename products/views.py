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

from prometeo.core.details import ModelDetails, ModelPaginatedListDetails
from prometeo.core.paginator import paginate

from models import *
from forms import *

def uom_index(request):
    """Show a UOM list.
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
        
    uoms = ModelPaginatedListDetails(request, uoms)
        
    return render_to_response('products/uoms/index.html', RequestContext(request, {'uoms': uoms}))
     
def uom_add(request):
    """Add a new UOM.
    """
    if request.method == 'POST':
        form = UOMForm(request.POST)
        if form.is_valid():
            uom = form.save()
            return redirect_to(request, url='/products/uoms/view/%s/' % (uom.pk))
    else:
        form = UOMForm()

    return render_to_response('products/uoms/add.html', RequestContext(request, {'form': form}));
     
def uom_view(request, id):
    """Show UOM details.
    """
    uom = get_object_or_404(UOM, pk=id)
    details = ModelDetails(instance=uom)
    return render_to_response('products/uoms/view.html', RequestContext(request, {'uom': uom, 'details': details}))
     
def uom_edit(request, id):
    """Edit a UOM.
    """
    uom = get_object_or_404(UOM, pk=id)
    if request.method == 'POST':
        form = UOMForm(request.POST, instance=uom)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/products/uoms/view/%s/' % (id))
    else:
        form = UOMForm(instance=uom)
    return render_to_response('products/uoms/edit.html', RequestContext(request, {'uom': uom, 'form': form}))
    
def uom_delete(request, id):
    """Delete a UOM.
    """
    uom = get_object_or_404(UOM, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            uom.delete()
            return redirect_to(request, url='/products/uoms/');
        return redirect_to(request, url='/products/uoms/view/%s/' % (id))
    return render_to_response('products/uoms/delete.html', RequestContext(request, {'uom': uom}))
 
def uom_category_index(request):
    """Show a UOM category list.
    """
    categories = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        categories = UOMCategory.objects.filter(queryset)
    else:
        categories = UOMCategory.objects.all()
        
    categories = ModelPaginatedListDetails(request, categories)
        
    return render_to_response('products/uoms/categories/index.html', RequestContext(request, {'categories': categories}))
     
def uom_category_add(request):
    """Add a new UOM category.
    """
    if request.method == 'POST':
        form = UOMCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect_to(request, url='/products/uoms/categories/view/%s/' % (category.pk))
    else:
        form = UOMCategoryForm()

    return render_to_response('products/uoms/categories/add.html', RequestContext(request, {'form': form}));
     
def uom_category_view(request, id):
    """Show UOM category details.
    """
    category = get_object_or_404(UOMCategory, pk=id)
    details = ModelDetails(instance=category)
    return render_to_response('products/uoms/categories/view.html', RequestContext(request, {'category': category, 'details': details}))
     
def uom_category_edit(request, id):
    """Edit a UOM category.
    """
    category = get_object_or_404(UOMCategory, pk=id)
    if request.method == 'POST':
        form = UOMCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/products/uoms/categories/view/%s/' % (id))
    else:
        form = CategoryForm(instance=category)
    return render_to_response('products/uoms/categories/edit.html', RequestContext(request, {'category': category, 'form': form}))
    
def uom_category_delete(request, id):
    """Delete a UOM category.
    """
    category = get_object_or_404(UOMCategory, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            category.delete()
            return redirect_to(request, url='/products/uoms/categories/');
        return redirect_to(request, url='/products/uoms/categories/view/%s/' % (id))
    return render_to_response('products/uoms/categories/delete.html', RequestContext(request, {'category': category}))
 
def product_index(request):
    """Show a product list.
    """
    products = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        products = Product.objects.filter(queryset)
    else:
        products = Product.objects.all()
        
    products = ModelPaginatedListDetails(request, products, exclude=['id', 'description', 'uos', 'uom_to_uos'])
        
    return render_to_response('products/index.html', RequestContext(request, {'products': products}))
     
def product_add(request):
    """Add a new product.
    """
    wizard = ProductWizard(template="products/add.html")
    return wizard(request)
     
def product_view(request, id):
    """Show product details.
    """
    product = get_object_or_404(Product, pk=id)
    details = ModelDetails(instance=product)
    return render_to_response('products/view.html', RequestContext(request, {'product': product, 'details': details}))
     
def product_edit(request, id):
    """Edit a product.
    """
    product = get_object_or_404(Product, pk=id)
    wizard = ProductWizard(initial=product, template="products/edit.html")
    return wizard(request)
    
def product_delete(request, id):
    """Delete a product.
    """
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            product.delete()
            return redirect_to(request, url='/products/');
        return redirect_to(request, url='/products/view/%s/' % (id))
    return render_to_response('products/delete.html', RequestContext(request, {'product': product}))
