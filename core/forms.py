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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import *
from django.conf import settings

from models import *

class AccountForm(forms.ModelForm):
    """Form for account data.
    """
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)
    language = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES)
    
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'is_superuser', 
                   'last_login', 'date_joined')
        
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            self.fields['language'].initial = kwargs['instance'].get_profile().language
        else:
            self.fields['language'].initial = settings.LANGUAGE_CODE

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
            
        return password2

    def save(self, commit=True):
        user = super(AccountForm, self).save(commit=False)
        self.save_m2m()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile = user.get_profile()
            profile.language = self.cleaned_data["language"]
            profile.save()
            
        return user
        
class AccountGroupForm(forms.ModelForm):
    """Form for account group data.
    """
    class Meta:
        model = AccountGroup
