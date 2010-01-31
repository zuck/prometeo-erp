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
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q

from prometeo.core.details import ModelDetails

from models import *
from forms import *

@login_required 
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
        
    return render_to_response('products/index.html', RequestContext(request, {'products': products}))
 
@login_required    
def product_add(request):
    """Add a new product.
    """
    wizard = ProductWizard(template="products/add.html")
    return wizard(request)

@login_required     
def product_view(request, id):
    """Show product details.
    """
    product = get_object_or_404(Product, pk=id)
    details = ModelDetails(instance=product)
    return render_to_response('products/view.html', RequestContext(request, {'product': product, 'details': details}))

@login_required     
def product_edit(request, id):
    """Edit a product.
    """
    product = get_object_or_404(Product, pk=id)
    wizard = ProductWizard(initial=product, template="products/edit.html")
    return wizard(request)

@login_required    
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
