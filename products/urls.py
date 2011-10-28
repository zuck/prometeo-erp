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
__version__ = '0.0.2'

from django.conf.urls.defaults import *

urlpatterns = patterns('products.views',

    # Products.
    url(r'^products/$', view='product_list', name='product_list'),
    url(r'^products/add/$', view='product_add', name='product_add'),
    url(r'^products/(?P<id>\d+)/$', view='product_detail', name='product_detail'),
    url(r'^products/(?P<id>\d+)/edit/$', view='product_edit', name='product_edit'),
    url(r'^products/(?P<id>\d+)/delete/$', view='product_delete', name='product_delete'),
    url(r'^products/(?P<id>\d+)/supplies/$', view='product_supplies', name='product_supplies'),
    url(r'^partners/(?P<id>\d+)/supplies/add/$', view='product_add_supply', name='product_add_supply'),
    url(r'^partners/(?P<product_id>\d+)/supplies/(?P<id>\d+)/$', view='product_supply_detail', name='product_supply_detail'),
    url(r'^partners/(?P<product_id>\d+)/supplies/(?P<id>\d+)/edit/$', view='product_edit_supply', name='product_edit_supply'),
    url(r'^partners/(?P<product_id>\d+)/supplies/(?P<id>\d+)/delete/$', view='product_delete_supply', name='product_delete_supply'),
    url(r'^products/(?P<id>\d+)/timeline/$', 'product_detail', {"template_name": "products/product_timeline.html"}, 'product_timeline'),
)
