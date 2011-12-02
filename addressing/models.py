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
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Address(models.Model):
    """Address model.
    """
    type = models.CharField(max_length=3, choices=settings.ADDRESS_TYPES, default=settings.DEFAULT_ADDRESS_TYPE, verbose_name=_('type'))
    street = models.CharField(max_length=255, verbose_name=_('street'))
    number = models.CharField(max_length=15, verbose_name=_('number'))
    city = models.CharField(max_length=255, verbose_name=_('city'))
    zip = models.CharField(max_length=255, verbose_name=_('zip code'))
    state = models.CharField(max_length=64, verbose_name=_('state/province'))
    country = models.CharField(max_length=64, verbose_name=_('country'))

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        
    def __unicode__(self):
        return _('%(number)s, %(street)s - %(city)s, %(state)s %(zip)s - %(country)s') % {
            'number': self.number,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'country': self.country
        }

class PhoneNumber(models.Model):
    """PhoneNumber model.
    """
    type = models.CharField(max_length=3, choices=settings.PHONE_TYPES, default=settings.DEFAULT_PHONE_TYPE, verbose_name=_('type'))
    number = models.CharField(max_length=30, verbose_name=_('number'))

    class Meta:
        verbose_name = _('phone number')
        verbose_name_plural = _('phone numbers')
        
    def __unicode__(self):
        return self.number

class SocialProfile(models.Model):
    """SocialProfile model.
    """
    network = models.CharField(max_length=5, choices=settings.SOCIAL_NETWORKS, default=settings.DEFAULT_SOCIAL_NETWORK, verbose_name=_('social network'))
    profile = models.CharField(max_length=30, verbose_name=_('profile'))

    class Meta:
        verbose_name = _('social profile')
        verbose_name_plural = _('social profiles')
        
    def __unicode__(self):
        return self.profile
