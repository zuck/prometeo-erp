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

from django import forms

from prometeo.core.forms import enrich_form
from prometeo.core.forms.widgets import *

from models import *

class ContactForm(forms.ModelForm):
    """Form for contact data.
    """
    class Meta:
        model = Contact
        exclude = ['id', 'addresses', 'phone_numbers', 'social_profiles', 'created', 'stream']
        widgets = {
            'date_of_birth': DateWidget(),
            'main_address': SelectAndAddWidget(add_url='/addresses/add/', with_perms=['addressing.add_address']),
            'main_phone_number': SelectAndAddWidget(add_url='/phones/add/', with_perms=['addressing.add_phonenumber']),
            'user': SelectAndAddWidget(add_url='/users/add/', with_perms=['auth.add_user']),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['main_address'].queryset = self.instance.addresses.all()
            self.fields['main_phone_number'].queryset = self.instance.phone_numbers.all()
        else:
            del self.fields['main_address']
            del self.fields['main_phone_number']

class ContactJobForm(forms.ModelForm):
    """Form for job data from a contact point of view.
    """
    class Meta:
        model = Job
        exclude = ['contact', 'created']
        widgets = {
            'started': DateWidget(),
            'ended': DateWidget(),
            'partner': SelectAndAddWidget(add_url='/partners/add/', with_perms=['partners.add_partner']),
        }

class PartnerForm(forms.ModelForm):
    """Form for partner data.
    """
    class Meta:
        model = Partner
        exclude = ['id', 'addresses', 'phone_numbers', 'social_profiles', 'contacts', 'dashboard', 'stream', 'author', 'created']
        widgets = {
            'description': CKEditor(),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        if Partner.objects.count() == 0:
            self.fields['is_managed'].initial = True
        if self.instance.pk:
            self.fields['main_address'].queryset = self.instance.addresses.all()
            self.fields['main_phone_number'].queryset = self.instance.phone_numbers.all()
        else:
            del self.fields['main_address']
            del self.fields['main_phone_number']

    def clean_vat_number(self):
        vat_number = self.cleaned_data['vat_number']
        if not vat_number:
            vat_number = None
        return vat_number    
        
class PartnerJobForm(forms.ModelForm):
    """Form for job data from a partner point of view.
    """
    class Meta:
        model = Job
        exclude = ['partner', 'created']
        widgets = {
            'started': DateWidget(),
            'ended': DateWidget(),
            'contact': SelectAndAddWidget(add_url='/contacts/add/', with_perms=['partners.add_contact']),
        }     
        
class LetterForm(forms.ModelForm):
    """Form for letter data.
    """
    class Meta:
        model = Letter
        widgets = {
            'date': DateWidget(),
            'target_ref_date': DateWidget(),
            'target': SelectAndAddWidget(add_url='/partners/add/', with_perms=['partners.add_partner']),
            'to': SelectAndAddWidget(add_url='/contacts/add/', with_perms=['partners.add_contact']),
            'body': CKEditor(),
        }

enrich_form(ContactForm)
enrich_form(ContactJobForm)
enrich_form(PartnerForm)
enrich_form(PartnerJobForm)
enrich_form(LetterForm)
