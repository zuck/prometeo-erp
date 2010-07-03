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
from prometeo.products.models import Supply

from models import Warehouse, Movement

class WarehouseForm(forms.ModelForm):
    """Form for warehouse data.
    """
    class Meta:
        model = Warehouse
        
class MovementVerseForm(forms.ModelForm):
    """Form for movement verse choice.
    """
    class Meta:
        model = Movement
        fields = ['verse']
        
class MovementProductForm(forms.ModelForm):
    """Form for outcome movement product choice.
    """
    class Meta:
        model = Movement
        fields = ['product']
        
    def __init__(self, *args, **kwargs):
        super(MovementProductForm, self).__init__(*args, **kwargs)
        if self.instance.verse == True:
            self.fields['supply'] = forms.ModelChoiceField(label=_('Product'), queryset=Supply.objects.all())
            del self.fields['product']

    def clean_product(self):
        product = self.cleaned_data['product']
        stock = self.instance.warehouse.stock(product)
        if stock == 0:
            raise forms.ValidationError(_("You're trying to send out a product which is not in the warehouse."))
        return product
            
    def clean_supply(self):
        supply = self.cleaned_data['supply']
        self.cleaned_data['product'] = supply.product
        return supply
        

class MovementDetailsForm(forms.ModelForm):
    """Form for movement data.
    """
    class Meta:
        model = Movement
        fields = ['quantity', 'unit_value']
        
    def __init__(self, *args, **kwargs):
        super(MovementDetailsForm, self).__init__(*args, **kwargs)
        if self.instance.verse == False:
            del self.fields['unit_value']
        
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        
        # Quantity <= 0: invalid value.
        if quantity <= 0:
            raise forms.ValidationError(_("The quantity must be greater than zero."))
            
        # Outcome movement: invalid if there are not enough stocks.
        elif self.instance.verse == False:
            product = self.instance.product
            stock = self.instance.warehouse.stock(product, exclude=[self.instance])
            if quantity > stock:
                uom = product.uom
                raise forms.ValidationError(_("You're trying to send out a quantity greater than the current stock (%(stock).2f%(uom)s).") % {'stock': stock, 'uom': uom})
            self.cleaned_data['unit_value'] = self.instance.warehouse.average_value(product, exclude=[self.instance])
                
        return quantity
        
class MovementWizard(wizard.FormWizard):
    """Form wizard for movement data.
    """
    def __init__(self, initial=None, template=None):
        form_list = [MovementVerseForm, MovementProductForm, MovementDetailsForm]
        super(MovementWizard, self).__init__(form_list, initial, template)
        
    def process_step(self, request, form, step):
        instance = form.instance

        # Step 0: verse choice.
        if step == 0:
            pass
        
        # Step 1: product choice.    
        elif step == 1:
        
            # Income movement.
            if instance.verse is True:
                supply = form.cleaned_data['supply']
                instance.product = supply.product
                instance.quantity = supply.minimal_quantity
                instance.unit_value = supply.final_price()
                
            # Outcome movement.
            else:
                product = form.cleaned_data['product']
                instance.product = product
                instance.quantity = instance.warehouse.stock(product)
                instance.unit_value = instance.warehouse.average_value(product, exclude=[instance])
                
    def done(self, request, form_list):
        movement = form_list[0].save(commit=False)
        movement.product = form_list[1].cleaned_data['product']
        movement.quantity = form_list[2].cleaned_data['quantity']
        movement.unit_value = form_list[2].cleaned_data['unit_value']
        movement.save()

        return redirect_to(request, url=movement.warehouse.get_movements_url())
