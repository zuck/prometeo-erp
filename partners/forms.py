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
from models import *
        
class RoleForm(forms.ModelForm):
    """Form for role data.
    """
    class Meta:
        model = Role

class ContactForm(forms.ModelForm):
    """Form for contact data.
    """
    class Meta:
        model = Contact
        exclude = ['id', 'addresses', 'telephones']

class ContactJobForm(forms.ModelForm):
    """Form for job data from a contact point of view.
    """
    class Meta:
        model = Job
        exclude = ['contact']

class PartnerForm(forms.ModelForm):
    """Form for partner data.
    """
    class Meta:
        model = Partner
        exclude = ['id', 'addresses', 'telephones', 'contacts']
        
class PartnerTelephoneForm(forms.ModelForm):
    """Form for a telephone number data.
    """
    class Meta:
        model = Telephone
        
class PartnerAddressForm(forms.ModelForm):
    """Form for a address data.
    """
    class Meta:
        model = Address
        
class PartnerJobForm(forms.ModelForm):
    """Form for job data from a partner point of view.
    """
    class Meta:
        model = Job
        exclude = ['partner']
