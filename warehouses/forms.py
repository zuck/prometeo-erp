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
from django.views.generic.simple import redirect_to
from django import forms

from prometeo.core import wizard

from models import Warehouse, Movement

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
        exclude = ['warehouse', 'on', 'account', 'quantity', 'price', 'discount', 'payment_delay']
        
class SupplyForm(forms.ModelForm):
    """Form for supply data.
    """
    class Meta:
        model = Movement
        fields = ['quantity', 'price', 'discount', 'payment_delay']
        
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        
        # <= 0: invalid value.
        if quantity <= 0:
            raise forms.ValidationError(_("The quantity must be greater than zero."))
            
        # out movement: invalid if there are not enough stocks.
        elif self.instance.verse == False:
            supply = self.instance.supply
            stock = self.instance.warehouse.stock(supply.product, exclude=[self.instance])
            if quantity > stock:
                uom = supply.product.uom
                raise forms.ValidationError(_("You're trying to send out a quantity greater than the current stock (%(stock).2f%(uom)s).") % {'stock': stock, 'uom': uom})
                
        return quantity
        
    def clean_price(self):
        # Out movement.
        price = self.cleaned_data['price']
        
        if self.instance.verse == False:
            supply = self.instance.supply
            price = self.instance.warehouse.average_price(supply.product, exclude=[self.instance])

        return price
        
    def clean_discount(self):
        # Out movement.
        discount = self.cleaned_data['discount']
        
        if self.instance.verse == False:
            discount = 0
            
        return discount
        
    def clean_payment_delay(self):
        # Out movement.
        payment_delay = self.cleaned_data['payment_delay']
        
        if self.instance.verse == False:
            payment_delay = 0
            
        return payment_delay
        
class MovementWizard(wizard.FormWizard):
    """Form wizard for movement data.
    """
    def __init__(self, initial=None, template=None):
        form_list = [MovementForm, SupplyForm]
        super(MovementWizard, self).__init__(form_list, initial, template)
        
    def process_step(self, request, form, step):
        if step == 0:
            instance = form.instance
            instance.verse = form.cleaned_data['verse']
            supply = form.cleaned_data['supply']
            instance.supply = supply
            instance.quantity = supply.minimal_quantity
            instance.price = supply.price
            instance.discount = supply.discount
            instance.payment_delay = supply.payment_delay
            
            if form.cleaned_data['verse'] == False:
                instance.quantity = instance.warehouse.stock(supply.product)
                self.form_list[1].base_fields['price'].widget = forms.widgets.HiddenInput()
                self.form_list[1].base_fields['discount'].widget = forms.widgets.HiddenInput()
                self.form_list[1].base_fields['payment_delay'].widget = forms.widgets.HiddenInput()
            else:
                self.form_list[1].base_fields['price'].widget = forms.widgets.TextInput()
                self.form_list[1].base_fields['discount'].widget = forms.widgets.TextInput()
                self.form_list[1].base_fields['payment_delay'].widget = forms.widgets.TextInput()
                
            self.initial[1] = instance
                
    def done(self, request, form_list):
        movement = form_list[0].save(commit=False)
        movement.quantity = form_list[1].cleaned_data['quantity']
        movement.price = form_list[1].cleaned_data['price']
        movement.discount = form_list[1].cleaned_data['discount']
        movement.payment_delay = form_list[1].cleaned_data['payment_delay']
        movement.save()

        return redirect_to(request, url=movement.warehouse.get_absolute_url())
