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

class UOMCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name=_('name'))
    
    def get_absolute_url(self):
        return '/products/uoms/categories/view/%d/' % self.pk
    
    def get_edit_url(self):
        return '/products/uoms/categories/edit/%d/' % self.pk
    
    def get_delete_url(self):
        return '/products/uoms/categories/delete/%d/' % self.pk
    
    def get_uoms_url(self):
        return self.get_absolute_url() + 'uoms/'
                
    def __unicode__(self):
        return self.name

class UOM(models.Model):
    id = models.AutoField(primary_key=True)
    initials = models.CharField(max_length=6, verbose_name=_('initials'))
    name = models.CharField(max_length=64, verbose_name=_('name'))
    category = models.ForeignKey(UOMCategory, verbose_name=_('category'))
    
    def get_absolute_url(self):
        return '/products/uoms/view/%d/' % self.pk
    
    def get_edit_url(self):
        return '/products/uoms/edit/%d/' % self.pk
    
    def get_delete_url(self):
        return '/products/uoms/delete/%d/' % self.pk
        
    def __unicode__(self):
        return self.initials
        
class Supply(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.Product')
    supplier = models.ForeignKey('partners.Partner', verbose_name=_('supplier'))
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name'))
    code = models.CharField(max_length=255, blank=True, verbose_name=_('code'))
    price = models.FloatField(verbose_name=_('price'))
    discount = models.FloatField(default=0, verbose_name=_('discount'))
    delivery_delay = models.PositiveIntegerField(default=1, verbose_name=_('delivery delay'))
    minimal_quantity = models.FloatField(default=1, verbose_name=_('minimal quantity'))
    payment_delay = models.PositiveIntegerField(verbose_name=_('payment delay'))
    
    def final_price(self):
        return self.price * (1 + self.discount / 100)
        
    def get_edit_url(self):
        return '/products/%d/supplies/edit/%d/' % (self.product.pk, self.pk)
    
    def get_delete_url(self):
        return '/products/%d/supplies/delete/%d/' % (self.product.pk, self.pk)
        
    def __unicode__(self):
        return '%s (%s) (%s %s%%)' % (self.product, self.supplier, self.price, self.discount)

class Product(models.Model):   
    PRODUCT_TYPES = (
        ('0', _('Consumable')),
        ('1', _('Stockable'))
    )

    PRODUCT_SUPPLY_METHODS = (
        ('0', _('Purchase')),
        ('1', _('Production'))
    )        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_('name'))
    code = models.CharField(max_length=255, verbose_name=_('code'))
    ean13 = models.CharField(max_length=13, blank=True, verbose_name=_('EAN13'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    uom = models.ForeignKey(UOM, verbose_name=_('UOM'))
    uos = models.ForeignKey(UOM, related_name='product_uos_set', verbose_name=_('UOS'))
    uom_to_uos = models.FloatField(default=1, verbose_name=_('UOM to UOS'))
    type = models.CharField(max_length=1, choices=PRODUCT_TYPES, verbose_name=_('type'))
    supply_method = models.CharField(max_length=1, choices=PRODUCT_SUPPLY_METHODS, verbose_name=_('supply method'))
    suppliers = models.ManyToManyField('partners.Partner', through=Supply, verbose_name=_('suppliers'))
    
    def get_absolute_url(self):
        return '/products/view/%d/' % self.pk
    
    def get_edit_url(self):
        return '/products/edit/%d/' % self.pk
    
    def get_delete_url(self):
        return '/products/delete/%d/' % self.pk
    
    def get_supplies_url(self):
        return self.get_absolute_url() + 'supplies/'
    
    def get_add_supply_url(self):
        return '/products/%d/supplies/add' % self.pk
        
    def __unicode__(self):
        return self.name
