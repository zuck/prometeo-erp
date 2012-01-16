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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

from prometeo.core.forms import enrich_form

from models import *

class UserEditForm(forms.ModelForm):
    """Form for user data.
    """
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'date_joined')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = (self.instance.pk is None)
        self.fields['password2'].required = (self.instance.pk is None)
        self.fields['email'].required = True

        if (self.instance.pk is None):
            del self.fields['user_permissions']

    def clean_password1(self):
        """Checks for a valid password1.
        """
        password1 = self.cleaned_data["password1"]
            
        if not (password1 or self.instance.pk):
            raise forms.ValidationError(_('This field is required.'))
            
        return password1

    def clean_password2(self):
        """Checks if password2 is equal to password1.
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2 and (password2 or not self.instance.pk):
            raise forms.ValidationError(_("The two password fields didn't match."))
            
        if not (password2 or self.instance.pk):
            raise forms.ValidationError(_('This field is required.'))
            
        return password2
        
    def clean_email(self):
        """Checks if the email address is unique.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']).exclude(pk=self.instance.pk):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        if self.cleaned_data['password1'] or not user.password:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()   
        return user

class UserProfileForm(forms.ModelForm):
    """Form for user's profile data.
    """
    class Meta:
        model = UserProfile
        exclude = ('user', 'dashboard', 'bookmarks', 'calendar')

enrich_form(UserEditForm)
enrich_form(UserProfileForm)
