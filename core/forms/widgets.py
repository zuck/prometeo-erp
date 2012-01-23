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

from datetime import time
from time import strptime, strftime
import json

from django import forms
from django.forms.widgets import flatatt
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.db import models

class DateWidget(forms.DateInput):
    """A more-friendly date widget with a pop-up calendar.
    """
    class Media:
        css = {
            "screen": ("css/blitzer/jquery-ui.custom.css",)
        }
        js = (
            "js/jquery.min.js",
            "js/jquery-ui.custom.min.js",
            "js/splitdatetime.js",
        )

    def __init__(self, attrs=None):
        self.date_class = 'datepicker'
        if not attrs:
            attrs = {}
        if 'date_class' in attrs:
            self.date_class = attrs.pop('date_class')
        if 'class' not in attrs:
            attrs['class'] = 'date'

        super(DateWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        return '<span class="%s">%s</span>' % (self.date_class, super(DateWidget, self).render(name, value, attrs))

class TimeWidget(forms.MultiWidget):
    """A more-friendly time widget.
    """
    def __init__(self, attrs=None):
        self.time_class = 'timepicker'
        if not attrs:
            attrs = {}
        if 'time_class' in attrs:
            self.time_class = attrs.pop('time_class')
        if 'class' not in attrs:
            attrs['class'] = 'time'

        widgets = (
            forms.Select(attrs=attrs, choices=[(i+1, "%02d" % (i+1)) for i in range(0, 12)]),
            forms.Select(attrs=attrs, choices=[(i, "%02d" % i) for i in range(0, 60)]),
            forms.Select(attrs=attrs, choices=[('AM', _('AM')),('PM', _('PM'))])
        )

        super(TimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, basestring):
            t, sep1, meridian = value.rpartition(' ')
            hour, sep2, minute = t.rpartition(':')
            return (int(hour), int(minute), meridian)
        return (None, None, None)

    def value_from_datadict(self, data, files, name):
        value = super(TimeWidget, self).value_from_datadict(data, files, name)
        t = strptime("%02d:%02d %s" % (int(value[0]), int(value[1]), value[2]), "%I:%M %p")
        return strftime("%H:%M:%S", t)

    def format_output(self, rendered_widgets):
        return '<span class="%s">%s%s%s</span>' % (
            self.time_class,
            rendered_widgets[0], rendered_widgets[1], rendered_widgets[2]
        )

class DateTimeWidget(forms.SplitDateTimeWidget):
    """A more-friendly date/time widget.

    Inspired by:

    http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/
    """
    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(DateTimeWidget, self).__init__(attrs, date_format, time_format)
        self.widgets = (
            DateWidget(attrs=attrs),
            TimeWidget(attrs=attrs),
        )

    def decompress(self, value):
        if value:
            d = strftime("%Y-%m-%d", value.timetuple())
            t = strftime("%I:%M %p", value.timetuple())
            return (d, t)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        return '%s<br/>%s' % (rendered_widgets[0], rendered_widgets[1])

class AddLinkMixin(object):
    class Media:
        css = {
            "screen": ("css/blitzer/jquery-ui.custom.css",)
        }
        js = (
            "js/jquery.min.js",
            "js/jquery-ui.custom.min.js",
            "js/addlink.js",
        )
    def add_link_decorator(self, render_func):
        def _wrapped_render(name, *args, **kwargs):
            output = render_func(name, *args, **kwargs)
            if self.add_url:
                tokens = {
                    'name': name,
                    'add_url': self.add_url,
                    'label': _('Add'),
                }
                output += '<a id="add-%(name)s-link" title="%(label)s" target="_blank" href="%(add_url)s">%(label)s</a>\n' % tokens
            return mark_safe('<span id="add-%(name)s" class="add">\n%(output)s\n<br/>\n</span>' % {'name': name, 'output': output})
        return _wrapped_render

class SelectAndAddWidget(forms.Select, AddLinkMixin):
    """A select widget with an optional "add" link.

    add_url -- link to the "add" action.    
    """
    def __init__(self, *args, **kwargs):
        self.add_url = kwargs.pop('add_url', None)
        super(SelectAndAddWidget, self).__init__(*args, **kwargs)
        self.render = self.add_link_decorator(self.render)

class SelectMultipleAndAddWidget(forms.SelectMultiple, AddLinkMixin):
    """A multiple-select widget with an optional "add" link.

    add_url -- link to the "add" action.    
    """
    def __init__(self, *args, **kwargs):
        self.add_url = kwargs.pop('add_url', None)
        super(SelectMultipleAndAddWidget, self).__init__(*args, **kwargs)
        self.render = self.add_link_decorator(self.render)

class JsonPairWidget(forms.Widget):
    """A widget that displays a list of text key/value pairs.

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
            data = json.loads(force_unicode(value))
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
            jsontext = json.dumps(data)
        return jsontext

class CKEditor(forms.Textarea):
    """A wrapper for the powerful CKEditor.
    """
    class Media:
        js = ('js/ckeditor/ckeditor.js',)

    def render(self, name, value, attrs={}):
        rendered = super(CKEditor, self).render(name, value, attrs)
        tokens = {
            'name': name,
            'toolbar': attrs.get('toolbar', 'Full'),
            'height': attrs.get('height', '220'),
            'width': attrs.get('width', '665'),
        }
        rendered += mark_safe(u'<script type="text/javascript">\n'                                              \
                              u'   CKEDITOR.replace("%(name)s",\n'                                              \
                              u'       {\n'                                                                     \
                              u'           toolbar: "%(toolbar)s",\n'                                           \
                              u'           height: "%(height)s",\n'                                             \
                              u'           width: "%(width)s",\n'                                               \
                              u'       }\n'                                                                     \
                              u'   );\n'                                                                        \
                              u'</script>\n' % tokens)
        return rendered
