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
from django.utils.translation import ugettext
from django.db import models
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)
    
    def get_absolute_url(self):
        return '/products/categories/view/%d' % self.id
        
    def __unicode__(self):
        buffer = ugettext(self.name)
        if (self.parent):
            buffer = self.parent.__unicode__() + ' / ' + buffer
            
        return buffer
        
PRODUCT_TYPES = (
    ('0', _('Consumable')),
    ('1', _('Stockable'))
)

PRODUCT_SUPPLY_METHODS = (
    ('0', _('Purchase')),
    ('1', _('Production'))
)

class Product(models.Model):        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64)
    ean13 = models.CharField(max_length=11, blank=True)
    description = models.TextField(blank=True)
    uom = models.ForeignKey('uoms.UOM')
    uos = models.ForeignKey('uoms.UOM', related_name='product_uos_set')
    uom_to_uos = models.FloatField(default=1)
    suppliers = models.ManyToManyField('partners.Partner')
    category = models.ForeignKey(Category, null=True, blank=True)
    type = models.CharField(max_length=1, choices=PRODUCT_TYPES)
    supply_method = models.CharField(max_length=1, choices=PRODUCT_SUPPLY_METHODS)
    
    def get_absolute_url(self):
        return '/products/view/%d' % self.id
        
    def __unicode__(self):
        return self.name
