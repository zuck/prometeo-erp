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

from django import forms
from django.forms.models import inlineformset_factory
from django.views.generic.simple import redirect_to

from prometeo.core import wizard

from models import *

class UOMForm(forms.ModelForm):
    """Form for uom data.
    """
    class Meta:
        model = UOM

class UOMCategoryForm(forms.ModelForm):
    """Form for uom category data.
    """
    class Meta:
        model = UOMCategory

class ProductForm(forms.ModelForm):
    """Form for product data.
    """
    class Meta:
        model = Product
        exclude = ['suppliers']
        
SupplyFormset = inlineformset_factory(Product, Supply, exclude=['product'], extra=1, can_delete=True)
        
class ProductWizard(wizard.FormWizard):
    """Form wizard for product data.
    """
    def __init__(self, initial=None, template=None):
        form_list = [ProductForm, SupplyFormset]
        super(ProductWizard, self).__init__(form_list, initial, template)
        
    def done(self, request, form_list):
        # 1) Save product.
        product = form_list[0].save(commit=False)
        try:
            product.pk = self.initial[0].pk
        except KeyError:
            pass
        product.save()
        
        # 2) Save supplies.
        supplies = form_list[1].save(commit=False)
        for supply in supplies:
            supply.product = product
            supply.save()
        
        return redirect_to(request, url=product.get_absolute_url())
