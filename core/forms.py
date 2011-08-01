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

from time import strftime

from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.forms.extras.widgets import *

class Form(forms.Form):
    """Base form.
    """
    required_css_class = 'required'
    error_css_class = 'errors'

class ModelForm(forms.ModelForm):
    """Base model form.
    """
    required_css_class = 'required'
    error_css_class = 'errors'

class SelectMultipleAndAddWidget(forms.SelectMultiple):
    """A multiple-select widget with an optional "add" link.
    """
    def __init__(self, *args, **kwargs):
        self.add_url = ""
        if kwargs.has_key('add_url'):
            self.add_url = kwargs['add_url']
            del kwargs['add_url']
        super(SelectMultipleAndAdd, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        output = super(SelectMultipleAndAdd, self).render(name, value, attrs, choices)
        if self.add_url:
            output += '<span class="add"><a target="_blank" href="%s">+</a></span><br/>' % self.add_url
        return mark_safe(output)
