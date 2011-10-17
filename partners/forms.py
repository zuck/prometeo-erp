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

from prometeo.core.forms import enrich_form
from prometeo.core.forms.widgets import *

from models import *

class ContactForm(forms.ModelForm):
    """Form for contact data.
    """
    class Meta:
        model = Contact
        exclude = ['id', 'addresses', 'phone_numbers']
        widgets = {
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['main_address'].queryset = self.instance.addresses.all()
        self.fields['main_phone_number'].queryset = self.instance.phone_numbers.all()

class ContactJobForm(forms.ModelForm):
    """Form for job data from a contact point of view.
    """
    class Meta:
        model = Job
        exclude = ['contact']
        widgets = {
            'partner': SelectAndAddWidget(add_url='/partners/add/'),
        }

class PartnerForm(forms.ModelForm):
    """Form for partner data.
    """
    class Meta:
        model = Partner
        exclude = ['id', 'addresses', 'phone_numbers', 'contacts', 'dashboard', 'stream']
        widgets = {
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.fields['main_address'].queryset = self.instance.addresses.all()
        self.fields['main_phone_number'].queryset = self.instance.phone_numbers.all()
        
class PartnerJobForm(forms.ModelForm):
    """Form for job data from a partner point of view.
    """
    class Meta:
        model = Job
        exclude = ['partner']
        widgets = {
            'contact': SelectAndAddWidget(add_url='/partners/contacts/add/'),
        }

enrich_form(ContactForm)
enrich_form(ContactJobForm)
enrich_form(PartnerForm)
enrich_form(PartnerJobForm)
