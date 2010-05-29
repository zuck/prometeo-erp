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

class Address(models.Model):
    ADDRESS_TYPES = (
        ('0', _('preferred')),
        ('1', _('invoice')),
        ('2', _('delivery')),
        ('3', _('other'))
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1, choices=ADDRESS_TYPES, default='0', verbose_name=_('type'))
    street = models.CharField(max_length=255, verbose_name=_('street'))
    number = models.CharField(max_length=15, verbose_name=_('number'))
    city = models.CharField(max_length=255, verbose_name=_('city'))
    zip = models.CharField(max_length=255, verbose_name=_('zip'))
    state = models.CharField(max_length=64, verbose_name=_('state/province'))
    country = models.CharField(max_length=64, verbose_name=_('country'))
        
    def __unicode__(self):
        return _('%(number)s, %(street)s - %(city)s, %(state)s %(zip)s - %(country)s') % {'number': self.number, 'street': self.street, 'city': self.city, 'state': self.state, 'zip': self.zip, 'country': self.country}

class Telephone(models.Model):
    PHONE_TYPES = (
        ('0', _('land Line')),
        ('1', _('mobile')),
        ('2', _('fax'))
    )
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30, verbose_name=_('number'))
    type = models.CharField(max_length=1, choices=PHONE_TYPES, default='0', verbose_name=_('type'))
        
    def __unicode__(self):
        return self.number
    
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_('name'))
    
    def get_absolute_url(self):
        return '/partners/contacts/roles/view/%d/' % self.pk
    
    def get_edit_url(self):
        return '/partners/contacts/roles/edit/%d/' % self.pk
    
    def get_delete_url(self):
        return '/partners/contacts/roles/delete/%d/' % self.pk
        
    def __unicode__(self):
        return self.name

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.SlugField(null=True, blank=True, verbose_name=_('nickname'))
    firstname = models.CharField(max_length=255, verbose_name=_('firstname'))
    lastname = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('lastname'))
    ssn = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('SSN'))
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name=_('email'))
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name=_('url'))
    addresses = models.ManyToManyField(Address, blank=True, verbose_name=_('addresses'))
    telephones = models.ManyToManyField(Telephone, blank=True, verbose_name=_('telephone numbers'))
    
    def get_absolute_url(self):
        return '/partners/contacts/view/%d/' % self.pk
    
    def get_edit_url(self):
        return '/partners/contacts/edit/%d/' % self.pk
    
    def get_delete_url(self):
        return '/partners/contacts/delete/%d/' % self.pk
    
    def get_jobs_url(self):
        return self.get_absolute_url() + 'jobs/'
    
    def get_add_job_url(self):
        return '/partners/contacts/%d/jobs/add/' % self.pk
        
    def __unicode__(self):
        if self.nickname:
            return self.nickname
        return ' '.join([self.firstname, self.lastname])

class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    managed = models.BooleanField(default=False, verbose_name=_('managed'))
    customer = models.BooleanField(default=False, verbose_name=_('customer'))
    supplier = models.BooleanField(default=False, verbose_name=_('supplier'))
    vat_number = models.CharField(max_length=64, unique=True, verbose_name=_('VAT number'))
    url = models.URLField(blank=True, verbose_name=_('url'))
    email = models.EmailField(blank=True, verbose_name=_('email'))
    addresses = models.ManyToManyField(Address, blank=True, verbose_name=_('addresses'))
    telephones = models.ManyToManyField(Telephone, blank=True, verbose_name=_('telephone numbers'))
    contacts = models.ManyToManyField(Contact, through='partners.Job', blank=True, verbose_name=_('contacts'))
    
    def get_absolute_url(self):
        return '/partners/view/%d/' % self.pk
    
    def get_edit_url(self):
        return '/partners/edit/%d/' % self.pk
    
    def get_delete_url(self):
        return '/partners/delete/%d/' % self.pk
        
    def get_telephones_url(self):
        return self.get_absolute_url() + 'telephones/'
        
    def get_add_telephone_url(self):
        return '/partners/%d/telephones/add/' % self.pk
        
    def get_addresses_url(self):
        return self.get_absolute_url() + 'addresses/'
        
    def get_add_address_url(self):
        return '/partners/%d/addresses/add/' % self.pk
        
    def get_contacts_url(self):
        return self.get_absolute_url() + 'contacts/'
        
    def get_add_contact_url(self):
        return '/partners/%d/contacts/add/' % self.pk
        
    def __unicode__(self):
        return self.name
        
class PartnerAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address)
    partner = models.ForeignKey(Partner)
    note = models.TextField()
        
class PartnerTelephoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    telephone = models.ForeignKey(Telephone)
    partner = models.ForeignKey(Partner)
    note = models.TextField()
        
class Job(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(Contact)
    partner = models.ForeignKey(Partner)
    role = models.ForeignKey(Role)
        
    def __unicode__(self):
        return _("%(contact)s as %(role)s for %(partner)s") % {'contact': self.contact, 'role': self.role, 'partner': self.partner}
