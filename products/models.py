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

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from prometeo.core.models import Commentable

class Product(Commentable):
    """Product model.
    """
    name = models.CharField(max_length=255, verbose_name=_('name'))
    code = models.CharField(max_length=255, verbose_name=_('code'))
    ean13 = models.CharField(max_length=13, blank=True, verbose_name=_('EAN13'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    uom = models.CharField(max_length=20, choices=settings.PRODUCT_UOM_CHOICES, default=settings.PRODUCT_DEFAULT_UOM, verbose_name=_('UOM'))
    uos = models.CharField(max_length=20, choices=settings.PRODUCT_UOM_CHOICES, default=settings.PRODUCT_DEFAULT_UOM, verbose_name=_('UOS'))
    uom_to_uos = models.FloatField(default=1.0, help_text=_('Conversion rate between UOM and UOS'), verbose_name=_('UOM to UOS'))
    weight = models.FloatField(default=1.0, verbose_name=_('unit weight (Kg)'))
    is_consumable = models.BooleanField(default=False, verbose_name=_('consumable?'))
    is_service = models.BooleanField(default=False, verbose_name=_('service?'))
    sales_price = models.FloatField(default=0.0, verbose_name=_('sales price'))
    sales_currency = models.CharField(max_length=3, choices=settings.CURRENCIES, default=settings.DEFAULT_CURRENCY, verbose_name=_('sales currency'))
    max_sales_discount = models.FloatField(default=0.0, verbose_name=_('max sales discount (%)'))
    sales_tax = models.FloatField(default=0.0, verbose_name=_('sales tax (%)'))
    suppliers = models.ManyToManyField('partners.Partner', through='products.Supply', null=True, blank=True, verbose_name=_('suppliers'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_("dashboard"))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering = ('code',)
        verbose_name = _('product')
        verbose_name_plural = _('products')
        
    def __unicode__(self):
        return '#%s: %s' % (self.code, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', (), {"id": self.pk})
    
    @models.permalink
    def get_edit_url(self):
        return ('product_edit', (), {"id": self.pk})
    
    @models.permalink
    def get_delete_url(self):
        return ('product_delete', (), {"id": self.pk})

class ProductEntry(models.Model):
    """A set of instances of the same product.
    """
    product = models.ForeignKey(Product, verbose_name=_('product'))
    quantity = models.FloatField(default=1.0, verbose_name=_('quantity'))
    unit_price = models.FloatField(null=True, blank=True, help_text=_("Keep it blank to use the product's default one"), verbose_name=_('unit price'))
    tax = models.FloatField(null=True, blank=True, help_text=_("Keep it blank to use the product's default one"), verbose_name=_('tax (%)'))
    discount = models.FloatField(null=True, blank=True, help_text=_("Keep it blank to use the product's default one"), verbose_name=_('discount (%)'))
    notes = models.TextField(null=True, blank=True, verbose_name=_('notes'))

    class Meta:
        verbose_name = _('product entry')
        verbose_name_plural = _('product entries')
        
    def __unicode__(self):
        return '%s (%d %s)' % (self.product, self.quantity, self.product.uos)

    def get_absolute_url(self):
        return self.product.get_absolute_url()
        
class Supply(models.Model):
    """Relation between a product and one of its supplier.
    """
    product = models.ForeignKey(Product, verbose_name=_('product'))
    supplier = models.ForeignKey('partners.Partner', limit_choices_to = {'is_supplier': True}, verbose_name=_('supplier'))
    supply_method = models.CharField(max_length=10, choices=settings.PRODUCT_SUPPLY_METHODS, default=settings.PRODUCT_DEFAULT_SUPPLY_METHOD, verbose_name=_('supply method'))
    name = models.CharField(max_length=255, null=True, blank=True, help_text=_("Product name used by the supplier"), verbose_name=_('ref. name'))
    code = models.CharField(max_length=255, null=True, blank=True, help_text=_("Product code used by the supplier"), verbose_name=_('ref. code'))
    purchase_price = models.FloatField(default=0.0, verbose_name=_('purchase price'))
    purchase_currency = models.CharField(max_length=3, choices=settings.CURRENCIES, default=settings.DEFAULT_CURRENCY, verbose_name=_('purchase currency'))
    max_purchase_discount = models.FloatField(default=0.0, verbose_name=_('max purchase discount (%)'))
    purchase_tax = models.FloatField(default=0.0, verbose_name=_('purchase tax (%)'))
    lead_time = models.PositiveIntegerField(default=1, verbose_name=_('lead time (days)'))
    minimal_quantity = models.FloatField(default=1.0, verbose_name=_('minimal quantity'))
    warranty_period = models.PositiveIntegerField(default=settings.PRODUCT_DEFAULT_WARRANTY_PERIOD, verbose_name=_('warranty period (days)'))
    end_of_life = models.DateField(null=True, blank=True, verbose_name=_('end of life'))

    class Meta:
        ordering = ('product', 'supplier')
        verbose_name = _('supply')
        verbose_name_plural = _('supplies')
        unique_together = (('product', 'supplier'),)
        
    def __unicode__(self):
        code = self.code or self.product.code
        name = self.name or self.product.name
        return '%s (%s)' % (self.product, self.supplier)

    @models.permalink
    def get_absolute_url(self):
        return ('product_supply_detail', (), {"product_id": self.product.pk, "id": self.pk})
    
    @models.permalink
    def get_edit_url(self):
        return ('product_edit_supply', (), {"product_id": self.product.pk, "id": self.pk})
    
    @models.permalink
    def get_delete_url(self):
        return ('product_delete_supply', (), {"product_id": self.product.pk, "id": self.pk})
