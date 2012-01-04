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

from models import *
from forms import *

def _get_product(request, *args, **kwargs):
    product_id = kwargs.get('product_id', None)
    id = kwargs.get('id', None)
    if product_id:
        return get_object_or_404(Product, id=product_id)
    elif id:
        return get_object_or_404(Product, id=id)
    return None

@permission_required('products.view_product')
def product_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a product list.
    """
    return filtered_list_detail(
        request,
        Product,
        fields=['name', 'code', 'ean13'],
        page=page,
        paginate_by=paginate_by,
        template_name='products/product_list.html',
        **kwargs
    )

@permission_required('products.add_product')     
def product_add(request, **kwargs):
    """Adds a new product.
    """
    product = Product()  
      
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, _("The product was created successfully."))
            return redirect_to(request, url=product.get_absolute_url())
    else:
        form = ProductForm(instance=product)

    return render_to_response('products/product_edit.html', RequestContext(request, {'form': form, 'object': product}))

@permission_required('products.view_product', _get_product)     
def product_detail(request, id, page=None, **kwargs):
    """Shows product details.
    """
    object_list = Product.objects.all()

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        **kwargs
    )

@permission_required('products.change_product', _get_product)     
def product_edit(request, id, **kwargs):
    """Edits a product.
    """
    return create_update.update_object(
        request,
        object_id=id,
        form_class=ProductForm,
        template_name='products/product_edit.html'
    )

@permission_required('products.delete_product', _get_product)    
def product_delete(request, id, **kwargs):
    """Deletes a product.
    """
    return create_update.delete_object(
        request,
        model=Product,
        object_id=id,
        post_delete_redirect=reverse('product_list'),
        template_name='products/product_delete.html',
        **kwargs
    )

@permission_required('products.view_product', _get_product) 
def product_supplies(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the product's supplies.
    """
    product = get_object_or_404(Product, pk=id)

    return filtered_list_detail(
        request,
        product.supply_set.all(),
        fields=['id', 'supplier', 'purchase_price', 'minimal_quantity', 'max_purchase_discount', 'payment_terms'],
        page=page,
        paginate_by=paginate_by,
        template_name='products/product_supplies.html',
        extra_context={'object': product},
        **kwargs
    )

@permission_required('products.change_product', _get_product)
def product_add_supply(request, id, **kwargs):
    """Adds a new supply to the given product.
    """
    supply = Supply(product_id=id)

    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=supply)
        if form.is_valid():
            form.save()
            messages.success(request, _("The supply was created successfully."))
            return redirect_to(request, url=supply.get_absolute_url())
    else:
        form = SupplyForm(instance=supply)

    return render_to_response('products/product_edit_supply.html', RequestContext(request, {'form': form, 'object': supply}))

@permission_required('products.view_product', _get_product)
def product_supply_detail(request, product_id, id, **kwargs):
    """Show details of the given product supply.
    """
    product = get_object_or_404(Product, pk=product_id)

    object_list = product.supply_set.all()

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        template_name='products/product_supply_detail.html',
        **kwargs
    )

@permission_required('products.change_product', _get_product)
def product_edit_supply(request, product_id, id, **kwargs):
    """Edits an supply of the given product.
    """
    supply = get_object_or_404(Supply, product__pk=product_id, pk=id)
    
    return create_update.update_object(
        request,
        form_class=SupplyForm,
        object_id=id,
        template_name='products/product_edit_supply.html',
        **kwargs
    )

@permission_required('products.change_product', _get_product)
def product_delete_supply(request, product_id, id, **kwargs):
    """Deletes an supply of the given product.
    """
    supply = get_object_or_404(Supply, product__pk=product_id, pk=id)
    
    return create_update.delete_object(
        request,
        model=Supply,
        object_id=id,
        post_delete_redirect=reverse('product_supplies', args=[product_id]),
        template_name='products/product_delete_supply.html',
        **kwargs
    )
