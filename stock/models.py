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

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from prometeo.core.utils import value_to_string

from managers import *

class Warehouse(models.Model):
    """Warehouse model.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    address = models.ForeignKey('addressing.Address', verbose_name=_('address'))
    owner = models.ForeignKey('partners.Partner', verbose_name=_('owner'))
    manager = models.ForeignKey('auth.User', null=True, blank=True, related_name='managed_warehouses', verbose_name=_('manager'))
    author = models.ForeignKey('auth.User', verbose_name=_('Created by'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_('dashboard'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))
    
    class Meta:
        ordering = ['owner', 'name']
        verbose_name = _('warehouse')
        verbose_name_plural = _('warehouses')
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('warehouse_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('warehouse_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('warehouse_delete', (), {"id": self.pk})

    def _value(self):
        value = 0.0
        for m in Movement.objects.for_warehouse(self):
            if m.origin == self:
                value -= m.value
            elif m.destination == self:
                value += m.value
        return value
    value = property(_value)
        
class Movement(models.Model):
    """Movement model.
    """
    origin = models.ForeignKey(Warehouse, related_name='origin_of_movements', verbose_name=_('origin warehouse'))
    destination = models.ForeignKey(Warehouse, related_name='destination_of_movements', verbose_name=_('destination warehouse'))
    product_entry = models.ForeignKey('products.ProductEntry', verbose_name=_('product'))
    author = models.ForeignKey('auth.User', verbose_name=_('Created by'))
    created = models.DateTimeField(auto_now=True, verbose_name=_('Created on'))

    objects = MovementManager()
    
    class Meta:
        ordering = ['-created']
        verbose_name = _('movement')
        verbose_name_plural = _('movements')
        
    def __unicode__(self):
        return "#%s of %s" % (self.id, value_to_string(self.created))

    @models.permalink
    def get_absolute_url(self):
        return ('movement_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('movement_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('movement_delete', (), {"id": self.pk})

    def _value(self):
        return self.product_entry.quantity * self.product_entry.unit_value
    value = property(_value)
