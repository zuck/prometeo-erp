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
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    """Form for editing a user's profile.
    """
    password1 = forms.CharField(label=_("Password"), required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), required=False, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'is_superuser', 
                   'groups', 'user_permissions', 'last_login', 'date_joined')

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
        if password1 != password2:
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
        """Saves the user's profile.
        """
        user = super(UserEditForm, self).save(commit=False)
        if self.cleaned_data['password1'] or not user.password:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()             
        return user

class UserRegistrationForm(UserEditForm):
    """Form for user registration.
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(), label=mark_safe(_(u'I have read and agree to the <a href="/terms-service" target="_blank">Terms of Service</a>')), error_messages={ 'required': u"You must agree to the terms to register." })
    pp = forms.BooleanField(widget=forms.CheckboxInput(), label=mark_safe(_(u'I have read and agree to the <a href="/privacy" target="_blank">Privacy Policy</a>')), error_messages={ 'required': u"You must agree to the privacy policy to register." })
    
class ContactForm(forms.Form):
    """A simple contact form.
    """
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())
    
    
