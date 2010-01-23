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
from django.utils.translation import ugettext_lazy as _

class Warehouse(models.Model):        
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('partners.Partner')
        
    def __unicode__(self):
        return self.name
        
class Movement(models.Model):        
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse)
    document = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('products.Product')
    quantity = models.IntegerField()
    user = models.ForeignKey('auth.User')
        
    def __unicode__(self):
        return _("%d %s of %s") % (self.quantity, self.product.uom, self.product)
        
    def verse(self):
        return (self.quantity >= 0)
