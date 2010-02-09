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

from django.conf.urls.defaults import *

urlpatterns = patterns('products.views',

    # Products.
    (r'^$', 'product_index'),
    (r'^add/$', 'product_add'),
    (r'^view/(?P<id>\d+)/(?P<page>\w*)/*$', 'product_view'),
    (r'^edit/(?P<id>\d+)/$', 'product_edit'),
    (r'^delete/(?P<id>\d+)/$', 'product_delete'),
    
    # Categories.
    (r'^categories/$', 'category_index'),
    (r'^categories/add/$', 'category_add'),
    (r'^categories/view/(?P<id>\d+)/(?P<page>\w*)/*$', 'category_view'),
    (r'^categories/edit/(?P<id>\d+)/$', 'category_edit'),
    (r'^categories/delete/(?P<id>\d+)/$', 'category_delete'),

    # UOMs.
    (r'^uoms/$', 'uom_index'),
    (r'^uoms/add/$', 'uom_add'),
    (r'^uoms/view/(?P<id>\d+)/$', 'uom_view'),
    (r'^uoms/edit/(?P<id>\d+)/$', 'uom_edit'),
    (r'^uoms/delete/(?P<id>\d+)/$', 'uom_delete'),
    
    # UOM Categories.
    (r'^uoms/categories/$', 'uom_category_index'),
    (r'^uoms/categories/add/$', 'uom_category_add'),
    (r'^uoms/categories/view/(?P<id>\d+)/(?P<page>\w*)/*$', 'uom_category_view'),
    (r'^uoms/categories/edit/(?P<id>\d+)/$', 'uom_category_edit'),
    (r'^uoms/categories/delete/(?P<id>\d+)/$', 'uom_category_delete'),
)
