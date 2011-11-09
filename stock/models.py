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

from prometeo.core.utils import value_to_string

from managers import *

class Warehouse(models.Model):
    """Warehouse model.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    owner = models.ForeignKey('partners.Partner', verbose_name=_('owner'))
    address = models.ForeignKey('addressing.Address', null=True, blank=True, verbose_name=_('address'))
    manager = models.ForeignKey('auth.User', null=True, blank=True, related_name='managed_warehouses', verbose_name=_('manager'))
    author = models.ForeignKey('auth.User', verbose_name=_('Created by'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_('dashboard'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))
    
    class Meta:
        ordering = ['owner', 'name']
        verbose_name = _('warehouse')
        verbose_name_plural = _('warehouses')
        
    def __unicode__(self):
        return _("%s (%s)") % (self.name, self.owner)

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
        return self.product_entry.quantity * self.product_entry.unit_price
    value = property(_value)

class DeliveryNote(models.Model):
    """Delivery note model.
    """
    invoice_addressee = models.ForeignKey('partners.Partner', related_name='invoice_addressee_of_delivery_notes', verbose_name=_('bill to'))
    delivery_addressee = models.ForeignKey('partners.Partner', null=True, blank=True, help_text=_('Keep it blank to use the same as invoicing'), related_name='delivery_addressee_of_delivery_notes', verbose_name=_('delivered to'))
    order_ref_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('order ref. no.'))
    order_ref_date = models.DateField(null=True, blank=True, verbose_name=_('on'))
    means_of_delivery = models.CharField(max_length=20, choices=settings.MEANS_OF_DELIVERY, default=settings.DEFAULT_MEAN_OF_DELIVERY, verbose_name=_('mean of delivery'))
    terms_of_payment = models.CharField(max_length=100, blank=True, choices=settings.TERMS_OF_PAYMENT, help_text=_("Keep it blank to use the owner's default one"), verbose_name=_('terms of payment'))
    reason_of_shipping = models.CharField(max_length=20, choices=settings.REASONS_OF_SHIPPING, default=settings.DEFAULT_REASON_OF_SHIPPING, verbose_name=_('reason of shipping'))
    terms_of_shipping = models.CharField(max_length=100, choices=settings.TERMS_OF_SHIPPING, default=settings.DEFAULT_TERMS_OF_SHIPPING, verbose_name=_('terms of shipping'))
    delivery_date = models.DateField(null=True, blank=True, verbose_name=_('delivery date'))
    goods_appearance = models.CharField(max_length=20, choices=settings.GOODS_APPEARANCES, default=settings.DEFAULT_GOODS_APPEARANCE, verbose_name=_('good appearance'))
    entries = models.ManyToManyField('products.ProductEntry', null=True, blank=True, verbose_name=_('entries'))
    notes = models.TextField(null=True, blank=True, verbose_name=_('notes'))
    
    class Meta:
        verbose_name = _('delivery note')
        verbose_name_plural = _('delivery notes')
        
    def __unicode__(self):
        return u'%s' % _('DN')

    @models.permalink
    def get_absolute_url(self):
        return ('deliverynote_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('deliverynote_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('deliverynote_delete', (), {"id": self.pk})
