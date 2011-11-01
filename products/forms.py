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

from django import forms
from django.forms import ValidationError
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse

from prometeo.core.forms import enrich_form
from prometeo.core.forms.widgets import *

from models import *

class ProductForm(forms.ModelForm):
    """Form for product data.
    """
    class Meta:
        model = Product
        exclude = ['suppliers', 'dashboard', 'stream']

class ProductEntryForm(forms.ModelForm):
    """Form for product entry data.
    """
    class Meta:
        model = ProductEntry
        widgets = {'product': SelectAndAddWidget(add_url='/products/add')}
        
class SupplyForm(forms.ModelForm):
    """Form for supply data.
    """
    class Meta:
        model = Supply
        exclude = ['product']
        widgets = {'end_of_life': DateWidget()}

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('product') # allow checking against the missing attribute

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)

_ProductEntryFormset = modelformset_factory(ProductEntry, form=ProductEntryForm, can_delete=True, extra=2)

class ProductEntryFormset(_ProductEntryFormset):
    def __init__(self, *args, **kwargs):
        super(ProductEntryFormset, self).__init__(*args, **kwargs)
        if len(self.forms) > 2:
            count = self.initial_form_count()+1
            self.forms = self.forms[:count]
            if count < self.total_form_count():
                for field in self.forms[-1].fields.values():
                    field.required = False
                self.forms[-1].fields['DELETE'].initial = True
            self.extra = 1

enrich_form(ProductForm)
enrich_form(ProductEntryForm)
enrich_form(SupplyForm)
