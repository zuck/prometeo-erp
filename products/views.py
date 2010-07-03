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
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.db.models import Q

from prometeo.core.details import ModelDetails, ModelPaginatedListDetails

from models import *
from forms import *

@permission_required('products.change_uom')
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
 
@permission_required('products.add_uom')    
def uom_add(request):
    """Add a new UOM.
    """
    if request.method == 'POST':
        form = UOMForm(request.POST)
        if form.is_valid():
            uom = form.save()
            return redirect_to(request, url=uom.get_absolute_url())
    else:
        form = UOMForm()

    return render_to_response('products/uoms/add.html', RequestContext(request, {'form': form}));

@permission_required('products.change_uom')   
def uom_view(request, id):
    """Show UOM details.
    """
    uom = get_object_or_404(UOM, pk=id)
    details = ModelDetails(instance=uom)
    return render_to_response('products/uoms/view.html', RequestContext(request, {'uom': uom, 'details': details}))

@permission_required('products.change_uom')     
def uom_edit(request, id):
    """Edit a UOM.
    """
    uom = get_object_or_404(UOM, pk=id)
    if request.method == 'POST':
        form = UOMForm(request.POST, instance=uom)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=uom.get_absolute_url())
    else:
        form = UOMForm(instance=uom)
    return render_to_response('products/uoms/edit.html', RequestContext(request, {'uom': uom, 'form': form}))

@permission_required('products.delete_uom')    
def uom_delete(request, id):
    """Delete a UOM.
    """
    uom = get_object_or_404(UOM, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            uom.delete()
            return redirect_to(request, url='/products/uoms/');
        return redirect_to(request, url=uom.get_absolute_url())
    return render_to_response('products/uoms/delete.html', RequestContext(request, {'uom': uom}))

@permission_required('products.change_uomcategory') 
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

@permission_required('products.add_uomcategory')     
def uom_category_add(request):
    """Add a new UOM category.
    """
    if request.method == 'POST':
        form = UOMCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect_to(request, url=category.get_absolute_url())
    else:
        form = UOMCategoryForm()

    return render_to_response('products/uoms/categories/add.html', RequestContext(request, {'form': form}));

@permission_required('products.change_uomcategory')      
def uom_category_view(request, id, page=None):
    """Show UOM category details.
    """
    category = get_object_or_404(UOMCategory, pk=id)
    
    # UOMs.
    if page == 'uoms':
        uoms = ModelPaginatedListDetails(request, category.uom_set.all(), exclude=['id', 'category_id'])
        return render_to_response('products/uoms/categories/uoms.html', RequestContext(request, {'category': category, 'uoms': uoms}))
        
    # Details.
    details = ModelDetails(instance=category)
    return render_to_response('products/uoms/categories/view.html', RequestContext(request, {'category': category, 'details': details}))

@permission_required('products.change_uomcategory')      
def uom_category_edit(request, id):
    """Edit a UOM category.
    """
    category = get_object_or_404(UOMCategory, pk=id)
    if request.method == 'POST':
        form = UOMCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=category.get_absolute_url())
    else:
        form = UOMCategoryForm(instance=category)
    return render_to_response('products/uoms/categories/edit.html', RequestContext(request, {'category': category, 'form': form}))

@permission_required('products.delete_uomcategory')     
def uom_category_delete(request, id):
    """Delete a UOM category.
    """
    category = get_object_or_404(UOMCategory, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            category.delete()
            return redirect_to(request, url='/products/uoms/categories/');
        return redirect_to(request, url=category.get_absolute_url())
    return render_to_response('products/uoms/categories/delete.html', RequestContext(request, {'category': category}))
    
@permission_required('products.change_product')  
def supply_index(request):
    """Show a supply list.
    """
    supplies = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        supplies = Supply.objects.filter(queryset)
    else:
        supplies = Supply.objects.all()
        
    supplies = ModelPaginatedListDetails(request, supplies, exclude=['id', 'name'])
        
    return render_to_response('products/supplies/index.html', RequestContext(request, {'supplies': supplies}))

@permission_required('products.change_product')  
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

@permission_required('products.add_product')      
def product_add(request):
    """Add a new product.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect_to(request, url=product.get_absolute_url())
    else:
        form = ProductForm()

    return render_to_response('products/add.html', RequestContext(request, {'form': form}));

@permission_required('products.change_product')      
def product_view(request, id, page=None):
    """Show product details.
    """
    product = get_object_or_404(Product, pk=id)
    
    # Supplies.
    if page == 'supplies':
        supplies = ModelPaginatedListDetails(request, product.supply_set.all(), exclude=['id', 'name', 'product_id'])
        return render_to_response('products/supplies.html', RequestContext(request, {'product': product, 'supplies': supplies}))
        
    # Details.
    details = ModelDetails(instance=product)
    return render_to_response('products/view.html', RequestContext(request, {'product': product, 'details': details}))

@permission_required('products.change_product')      
def product_edit(request, id):
    """Edit a product.
    """
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=product.get_absolute_url())
    else:
        form = ProductForm(instance=product)
    return render_to_response('products/edit.html', RequestContext(request, {'product': product, 'form': form}))

@permission_required('products.delete_product')     
def product_delete(request, id):
    """Delete a product.
    """
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            product.delete()
            return redirect_to(request, url='/products/');
        return redirect_to(request, url=product.get_absolute_url())
    return render_to_response('products/delete.html', RequestContext(request, {'product': product}))
    
@permission_required('products.change_product')
def product_add_supply(request, id):
    """Add a new supply for the product.
    """
    product = get_object_or_404(Product, pk=id)
    supply = Supply(product=product)
    
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=product.get_supplies_url())
    else:
        form = SupplyForm(instance=supply)

    return render_to_response('products/add_supply.html', RequestContext(request, {'product': product, 'form': form}));
    
@permission_required('products.change_product')      
def product_edit_supply(request, id, supply_id):
    """Edit a supply.
    """
    product = get_object_or_404(Product, pk=id)
    supply = get_object_or_404(Supply, pk=supply_id)
    if supply.product != product:
        raise Http404
    
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=product.get_supplies_url())
    else:
        form = SupplyForm(instance=supply)

    return render_to_response('products/edit_supply.html', RequestContext(request, {'product': product, 'supply': supply, 'form': form}));

@permission_required('products.change_product')     
def product_delete_supply(request, id, supply_id):
    """Delete a supply.
    """
    product = get_object_or_404(Product, pk=id)
    supply = get_object_or_404(Supply, pk=supply_id)
    if supply.product != product:
        raise Http404

    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            supply.delete()
        return redirect_to(request, url=product.get_supplies_url())
    return render_to_response('products/delete_supply.html', RequestContext(request, {'product': product, 'supply': supply})) 
