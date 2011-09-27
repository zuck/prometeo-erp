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

import simplejson
from time import strftime

from django import forms
from django.forms.widgets import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.db import models

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
        super(SelectMultipleAndAddWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        output = super(SelectMultipleAndAddWidget, self).render(name, value, attrs, choices)
        if self.add_url:
            output += '<span class="add"><a target="_blank" href="%s">%s</a></span><br/>' % (self.add_url, _('Add'))
        return mark_safe(output)

class JsonPairWidget(forms.Widget):
    """A widget that displays a list of text key/value pairs.

    kwargs:

    key_attrs -- html attributes applied to the 1st input box pairs
    val_attrs -- html attributes applied to the 2nd input box pairs

    Inspired by:

    http://www.huyng.com/archives/django-custom-form-widget-for-dictionary-and-tuple-key-value-pairs/
    """
    def __init__(self, *args, **kwargs):
        key_attrs = {}
        val_attrs = {}
        if "key_attrs" in kwargs:
            key_attrs = kwargs.pop("key_attrs")
        if "val_attrs" in kwargs:
            val_attrs = kwargs.pop("val_attrs")
        if "class" not in key_attrs:
            key_attrs['class'] = ''
        if "class" not in val_attrs:
            val_attrs['class'] = ''
        key_attrs['class'] = ' '.join(['json-key', key_attrs['class']]) 
        val_attrs['class'] = ' '.join(['json-val', val_attrs['class']]) 
        self.attrs = {'key_attrs': key_attrs, 'val_attrs': val_attrs}
        super(forms.Widget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        try:
            data = simplejson.loads(force_unicode(value))
        except:
            data = {}

        output = ''
        for k,v in data.items():
            output += self.render_pair(k, v, name)
        output += self.render_pair('', '', name)

        return mark_safe(output)

    def render_pair(self, key, value, name):
        ctx = {
            'key': key,
            'value': value,
            'fieldname': name,
            'key_attrs': flatatt(self.attrs['key_attrs']),
            'val_attrs': flatatt(self.attrs['val_attrs'])
        }
        return '<input type="text" name="json_key[%(fieldname)s]" value="%(key)s" %(key_attrs)s> <input type="text" name="json_value[%(fieldname)s]" value="%(value)s" %(val_attrs)s><br />' % ctx

    def value_from_datadict(self, data, files, name):
        jsontext = ""
        if data.has_key('json_key[%s]' % name) and data.has_key('json_value[%s]' % name):
            keys     = data.getlist("json_key[%s]" % name)
            values   = data.getlist("json_value[%s]" % name)
            data = {}
            for key, value in zip(keys, values):
                if len(key) > 0:
                    data[key] = value
            jsontext = simplejson.dumps(data)
        return jsontext
