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
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class BankAccount(models.Model):
    """Bank account model.
    """
    bank_name = models.CharField(max_length=255, verbose_name=_('bank name'))
    bic = models.CharField(max_length=20, verbose_name=_('BIC'))
    iban = models.CharField(max_length=30, verbose_name=_('IBAN'))
    owner = models.ForeignKey('partners.Partner', verbose_name=_('owner'))

    class Meta:
        verbose_name = _('bank account')
        verbose_name_plural = _('bank accounts')
        
    def __unicode__(self):
        return u'%s (%s)' % (self.iban, self.owner)

    @models.permalink
    def get_absolute_url(self):
        return ('bankaccount_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('bankaccount_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('bankaccount_delete', (), {"id": self.pk})
    
class SalesInvoice(models.Model):
    """Sales invoice model.
    """
    shipping_addressee = models.ForeignKey('partners.Partner', null=True, blank=True, related_name='shipping_addressee_of_salesinvoices', help_text=_('Keep it blank to use the same as invoicing'), verbose_name=_('ship to'))
    invoice_addressee = models.ForeignKey('partners.Partner', related_name='invoice_addressee_of_salesinvoices', verbose_name=_('bill to'))
    order_ref_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('order ref. no.'))
    order_ref_date = models.DateField(null=True, blank=True, verbose_name=_('order ref. date'))
    terms_of_shipping = models.CharField(max_length=100, choices=settings.TERMS_OF_SHIPPING, default=settings.DEFAULT_TERMS_OF_SHIPPING, verbose_name=_('terms of shipping'))
    amount = models.FloatField(default=0.0, verbose_name=_('amount'))
    terms_of_payment = models.CharField(max_length=100, choices=settings.TERMS_OF_PAYMENT, default=settings.DEFAULT_TERMS_OF_PAYMENT, verbose_name=_('terms of payment'))
    due_date = models.DateField(null=True, blank=True, verbose_name=_('due date'))
    bank_account = models.ForeignKey(BankAccount, verbose_name=_('bank account'))
    entries = models.ManyToManyField('products.ProductEntry', null=True, blank=True, verbose_name=_('entries'))
    notes = models.TextField(null=True, blank=True, verbose_name=_('notes'))

    class Meta:
        verbose_name = _('sales invoice')
        verbose_name_plural = _('sales invoices')
        
    def __unicode__(self):
        return u'%s' % _('INV')

    @models.permalink
    def get_absolute_url(self):
        return ('salesinvoice_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('salesinvoice_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('salesinvoice_delete', (), {"id": self.pk})
