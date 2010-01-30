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
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('partners.Partner', limit_choices_to={'is_mine': True})
    
    def value(self):
        value = 0
        for movement in self.movement_set.all():
            if movement.verse:
                value += movement.value()
            else:
                value -= movement.value()
        return value
        
    def stock(self, product, exclude=[]):
        queryset = Q(supply__product=product, warehouse=self)
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
        
    def average_price(self, product, exclude=[]):
        queryset = Q(supply__product=product, warehouse=self)
        movements = Movement.objects.filter(queryset)
        price = 0
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
            price = total / quantity
            
        return price

    def get_absolute_url(self):
        return '/warehouses/view/%d' % self.id
        
    def __unicode__(self):
        return self.name
        
class Movement(models.Model):
    MOVEMENT_VERSES = (
        (False, _('out')),
        (True, _('in'))
    )      
    id = models.AutoField(primary_key=True)
    verse = models.BooleanField(choices=MOVEMENT_VERSES, default=True)
    warehouse = models.ForeignKey(Warehouse)
    document = models.CharField(max_length=255, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    supply = models.ForeignKey('products.Supply')
    quantity = models.FloatField(default=1)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    payment_delay = models.PositiveIntegerField()
    last_user = models.ForeignKey('auth.User')
    
    class Meta:
        ordering = ['-last_modified']
    
    def is_last(self):
        return self == Movement.objects.filter(warehouse=self.warehouse).latest('id')
    
    def final_price(self):
        return self.price + (self.price * self.discount / 100)
    
    def value(self):
        return self.quantity * self.final_price()
    
    def get_absolute_url(self):
        return '/warehouses/movements/view/%d' % self.id
        
    def __unicode__(self):
        return _("%d%s of %s in %s, on %s") % (self.quantity, self.supply.product.uom, self.supply, self.warehouse, self.last_modified)
