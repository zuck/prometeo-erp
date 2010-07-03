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
from django.db import models
from django.db import connection
from django.db.models import Q

class Warehouse(models.Model):        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_('name'))
    owner = models.ForeignKey('partners.Partner', limit_choices_to={'managed': True}, verbose_name=_('owner'))
    
    def value(self):
        value = 0
        for movement in self.movement_set.all():
            if movement.verse:
                value += movement.value()
            else:
                value -= movement.value()
        return value
        
    def stock(self, product, exclude=[]):
        queryset = Q(product=product, warehouse=self)
        movements = Movement.objects.filter(queryset)
        stock = 0
        for movement in movements:
            if movement in exclude:
                continue
            if movement.verse:
                stock += movement.quantity
            else:
                stock -= movement.quantity
                
        return stock
        
    def average_value(self, product, exclude=[]):
        queryset = Q(product=product, warehouse=self)
        movements = Movement.objects.filter(queryset)
        value = 0
        total = 0
        quantity = 0
        for m in movements:
            if m in exclude:
                continue
            if m.verse:
                total += m.value()
                quantity += m.quantity
            else:
                total -= m.value()
                quantity -= m.quantity
        if quantity > 0:
            value = total / quantity
            
        return value

    def get_absolute_url(self):
        return '/warehouses/view/%d/' % self.pk

    def get_edit_url(self):
        return '/warehouses/edit/%d/' % self.pk

    def get_delete_url(self):
        return '/warehouses/delete/%d/' % self.pk

    def get_movements_url(self):
        return self.get_absolute_url() + 'movements/'

    def get_add_movement_url(self):
        return '/warehouses/%d/movements/add' % self.pk
        
    def __unicode__(self):
        return self.name
        
class Movement(models.Model):
    MOVEMENT_VERSES = (
        (False, _('outcome')),
        (True, _('income'))
    )      
    id = models.AutoField(primary_key=True)
    verse = models.BooleanField(choices=MOVEMENT_VERSES, default=True, verbose_name=_('verse'))
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('warehouse'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    quantity = models.FloatField(default=1, verbose_name=_('quantity'))
    unit_value = models.FloatField(verbose_name=_('unit value'))
    on = models.DateTimeField(auto_now=True, verbose_name=_('on'))
    
    class Meta:
        ordering = ['-on']
    
    def is_last(self):
        return self == Movement.objects.filter(warehouse=self.warehouse).latest('id')
    
    def value(self):
        return self.quantity * self.unit_value
    
    def get_absolute_url(self):
        return '/warehouses/%d/movements/view/%d/' % (self.warehouse.pk, self.pk)
    
    def get_edit_url(self):
        if self.is_last():
            return '/warehouses/%d/movements/edit/%d/' % (self.warehouse.pk, self.pk)
        return None
    
    def get_delete_url(self):
        if self.is_last():
            return '/warehouses/%d/movements/delete/%d/' % (self.warehouse.pk, self.pk)
        return None
        
    def __unicode__(self):
        if self.verse:
            return _("%(quantity)d%(uom)s of %(product)s to %(warehouse)s, on %(date)s") % {'quantity': self.quantity, 'uom': self.product.uom, 'product': self.product, 'warehouse': self.warehouse, 'date': self.on}
        return _("%(quantity)d%(uom)s of %(product)s from %(warehouse)s, on %(date)s") % {'quantity': self.quantity, 'uom': self.product.uom, 'product': self.product, 'warehouse': self.warehouse, 'date': self.on}
