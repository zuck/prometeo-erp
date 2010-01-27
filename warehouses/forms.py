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

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django import forms
from models import Warehouse, Movement
from django.db.models import Q

from prometeo.core import wizard

class WarehouseForm(forms.ModelForm):
    """Form for warehouse data.
    """
    class Meta:
        model = Warehouse
        
class MovementForm(forms.ModelForm):
    """Form for movement data.
    """
    class Meta:
        model = Movement
        exclude = ['warehouse', 'last_modified', 'last_user']
        
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        
        # <= 0: invalid value.
        if quantity <= 0:
            raise forms.ValidationError(_("The quantity must be greater than zero."))
            
        # out movement: invalid if there are not enough stocks.
        elif self.cleaned_data['verse'] == False:
            queryset = Q(product=self.cleaned_data['product'], warehouse=self.instance.warehouse)
            movements = Movement.objects.only('id', 'quantity', 'product').filter(queryset)
            stock = 0
            for movement in movements:
                stock += movement.quantity
            if quantity > stock:
                uom = self.cleaned_data['product'].uom
                raise forms.ValidationError(_("You're trying to send out a quantity greater than the current stock (%s%s).") % (stock, uom))
        return quantity
