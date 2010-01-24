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

from django.db import models

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return '/partners/contacts/view/%d' % self.id

class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_customer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    contacts = models.ManyToManyField(Contact, blank=True)
    
    def get_absolute_url(self):
        return '/partners/view/%d' % self.id
        
    def __unicode__(self):
        return self.name
