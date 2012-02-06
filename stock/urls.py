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

from django.conf.urls.defaults import *

urlpatterns = patterns('stock.views',

    # Warehouses.
    url(r'^warehouses/$', view='warehouses.warehouse_list', name='warehouse_list'),
    url(r'^warehouses/add/$', view='warehouses.warehouse_add', name='warehouse_add'),
    url(r'^warehouses/(?P<id>\d+)/$', view='warehouses.warehouse_detail', name='warehouse_detail'),
    url(r'^warehouses/(?P<id>\d+)/edit/$', view='warehouses.warehouse_edit', name='warehouse_edit'),
    url(r'^warehouses/(?P<id>\d+)/delete/$', view='warehouses.warehouse_delete', name='warehouse_delete'),
    url(r'^warehouses/(?P<id>\d+)/movements/$', view='warehouses.warehouse_movements', name='warehouse_movements'),
    url(r'^warehouses/(?P<id>\d+)/movements/ingoing/add/$', view='warehouses.warehouse_add_ingoing_movement', name='warehouse_add_ingoing_movement'),
    url(r'^warehouses/(?P<id>\d+)/movements/outgoing/add/$', view='warehouses.warehouse_add_outgoing_movement', name='warehouse_add_outgoing_movement'),
    url(r'^warehouses/(?P<id>\d+)/timeline/$', 'warehouses.warehouse_detail', {'template_name': 'stock/warehouse_timeline.html'}, 'warehouse_timeline'),

    # Movements.
    url(r'^movements/$', view='movements.movement_list', name='movement_list'),
    url(r'^movements/add$', view='movements.movement_add', name='movement_add'),
    url(r'^movements/(?P<id>\d+)/$', view='movements.movement_detail', name='movement_detail'),
    url(r'^movements/(?P<id>\d+)/edit/$', view='movements.movement_edit', name='movement_edit'),
    url(r'^movements/(?P<id>\d+)/delete/$', view='movements.movement_delete', name='movement_delete'),

    # Delivery notes.
    url(r'^deliverynotes/$', view='deliverynotes.deliverynote_list', name='deliverynote_list'),
    url(r'^deliverynotes/add$', view='deliverynotes.deliverynote_add', name='deliverynote_add'),
    url(r'^deliverynotes/(?P<id>\d+)/$', view='deliverynotes.deliverynote_detail', name='deliverynote_detail'),
    url(r'^deliverynotes/(?P<id>\d+)/edit/$', view='deliverynotes.deliverynote_edit', name='deliverynote_edit'),
    url(r'^deliverynotes/(?P<id>\d+)/delete/$', view='deliverynotes.deliverynote_delete', name='deliverynote_delete'),
    url(r'^deliverynotes/(?P<id>\d+)/hardcopies/$', view='deliverynotes.deliverynote_hardcopies', name='deliverynote_hardcopies'),
    url(r'^deliverynotes/(?P<id>\d+)/hardcopies/add/$', view='deliverynotes.deliverynote_add_hardcopy', name='deliverynote_add_hardcopy'),
    url(r'^deliverynotes/(?P<id>\d+)/timeline/$', 'deliverynotes.deliverynote_detail', {'template_name': 'stock/deliverynote_timeline.html'}, 'deliverynote_timeline'),
)
