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
__version__ = '$Revision: 19 $'

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.conf import settings
from django.contrib.formtools import wizard
from django.db import models
from django import forms
from django.forms.forms import BoundField
from django.forms.formsets import BaseFormSet
from django.utils.hashcompat import md5_constructor

# Inspired by http://code.google.com/p/wadofstuff/wiki/WadOfStuffDjangoForms

def security_hash(request, form, exclude=None, *args):
    """Calculates a security hash for the given Form/FormSet instance.

    This creates a list of the form field names/values in a deterministic
    order, pickles the result with the SECRET_KEY setting, then takes an md5
    hash of that.
    """

    data = []
    if exclude is None:
        exclude = ()
    if isinstance(form, BaseFormSet):
        for _form in form.forms + [form.management_form]:
            for bf in _form:
                if _form.empty_permitted and not _form.has_changed():
                    value = bf.data or ''
                else:
                    value = bf.field.clean(bf.data) or ''
                if isinstance(value, basestring):
                    value = value.strip()
                data.append((bf.name, value))
    else:
        for bf in form:
            if bf.name in exclude:
                continue
            if form.empty_permitted and not form.has_changed():
                value = bf.data or ''
            else:
                value = bf.field.clean(bf.data) or ''
            if isinstance(value, basestring):
                value = value.strip()
            data.append((bf.name, value))
    data.extend(args)
    data.append(settings.SECRET_KEY)

    # Use HIGHEST_PROTOCOL because it's the most efficient. It requires
    # Python 2.3, but Django requires 2.3 anyway, so that's OK.
    pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

    return md5_constructor(pickled).hexdigest()

class FormWizard(wizard.FormWizard):
    """Render prev_fields as a list of bound form fields in the template context.
    """
    def __init__(self, *args, **kwargs):
        super(FormWizard, self).__init__(*args, **kwargs)
        if isinstance(self.initial, models.Model):
            instance = self.initial
            self.initial = {}
            for i in range(self.num_steps()):
                self.initial[i] = instance
                
    def get_form(self, step, data=None):
        """Helper method that returns the Form/Formset instance for the given step.
        """
        initial = self.initial.get(step, None)
        form = self.form_list[step]
        if isinstance(initial, models.Model):
            return form(data, prefix=self.prefix_for_step(step), instance=initial)
        if isinstance(initial, models.query.QuerySet):
            return form(data, prefix=self.prefix_for_step(step), queryset=initial)
        
        return form(data, prefix=self.prefix_for_step(step), initial=initial)
        
    def security_hash(self, request, form):
        """Calculates the security hash for the given HttpRequest and
        Form/FormSet instances.

        Subclasses may want to take into account request-specific information,
        such as the IP address.
        """
        return security_hash(request, form)

    def render(self, form, request, step, context=None):
        """Renders the given Form object, returning an HttpResponse.
        """
        old_data = request.POST
        prev_fields = []
        if old_data:
            for i in range(step):
                old_form = self.get_form(i, old_data)
                hash_name = 'hash_%s' % i
                if isinstance(old_form, BaseFormSet):
                    for _form in old_form.forms + [old_form.management_form]:
                        prev_fields.extend([bf for bf in _form])
                else:
                    prev_fields.extend([bf for bf in old_form])
                hash_field = forms.Field(initial=old_data.get(hash_name,
                    self.security_hash(request, old_form)))
                bf = BoundField(forms.Form(), hash_field, hash_name)
                prev_fields.append(bf)
        return self.render_template(request, form, prev_fields, step, context)
