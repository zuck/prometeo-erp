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
import json

from django import forms
from django.forms.widgets import flatatt, Select, MultiWidget, DateInput, TextInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.db import models

class SplitDateTimeWidget(MultiWidget):
    """A more-friendly date/time widget.

    Inspired by:

    http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/
    """
    class Media:
        css = {
            "screen": ("css/blitzer/jquery-ui-1.8.16.custom.css",)
        }
        js = (
            "js/jquery-1.6.2.min.js",
            "js/jquery-ui-1.8.16.custom.min.js",
            "js/splitdatetime.js",
        )

    def __init__(self, attrs=None, date_format=None, time_format=None):
        if not attrs:
            attrs = {}

        try:
            date_class = attrs['date_class']
            del attrs['date_class']
        except:
            date_class = "datepicker"

        try:
            time_class = attrs['time_class']
            del attrs['time_class']
        except:
            time_class = "timepicker"

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        widgets = (
            DateInput(attrs=date_attrs, format=date_format),
            TextInput(attrs=time_attrs), TextInput(attrs=time_attrs),
            Select(attrs=time_attrs, choices=[('AM','AM'),('PM','PM')])
        )

        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = strftime("%Y-%m-%d", value.timetuple())
            hour = strftime("%I", value.timetuple())
            minute = strftime("%M", value.timetuple())
            meridian = strftime("%p", value.timetuple())
            return (d, hour, minute, meridian)
        else:
            return (None, None, None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return "%s: %s<br/>%s: %s%s%s" % (_("Date"), rendered_widgets[0], _("Time"), rendered_widgets[1], rendered_widgets[2], rendered_widgets[3])

class SelectMultipleAndAddWidget(forms.SelectMultiple):
    """A multiple-select widget with an optional "add" link.

    add_url -- link to the "add" action.    
    """
    class Media:
        css = {
            "screen": ("css/blitzer/jquery-ui-1.8.16.custom.css",)
        }
        js = (
            "js/jquery-1.6.2.min.js",
            "js/jquery-ui-1.8.16.custom.min.js"
        )

    def __init__(self, *args, **kwargs):
        self.add_url = ""
        if kwargs.has_key('add_url'):
            self.add_url = kwargs['add_url']
            del kwargs['add_url']
        super(SelectMultipleAndAddWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        output = super(SelectMultipleAndAddWidget, self).render(name, value, attrs, choices)
        if self.add_url:
            tokens = {
                'name': name,
                'add_url': self.add_url,
                'label': _('Add')
            }
            output += '<span id="add-%(name)s" class="add">'                                                                \
                      '    <a id="add-link-%(name)s" title="%(label)s" target="_blank" href="%(add_url)s">%(label)s</a>'    \
                      '</span>'                                                                                             \
                      '<script>'                                                                                            \
                      '    $("#add-link-%(name)s")'                                                                         \
                      '    .click('                                                                                         \
                      '        function(e) {'                                                                               \
                      '            e.preventDefault();'                                                                     \
                      '            $("#add-%(name)s")'                                                                      \
                      '            .append(\'<div id="add-dialog-%(name)s"></div>\')'                                       \
                      '            .children("#add-dialog-%(name)s")'                                                       \
                      '            .load("%(add_url)s #main")'                                                              \
                      '            .dialog({'                                                                               \
                      '                close: function(event, ui) { $("#add-dialog-%(name)s").remove(); },'                 \
                      '                modal: true,'                                                                        \
                      '                width: 360'                                                                          \
                      '             });'                                                                                    \
                      '         }'                                                                                          \
                      '    );'                                                                                              \
                      '</script>' % tokens
            output += '<br/>'
        return mark_safe(output)

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
            'skin': attrs.get('skin', 'v2'),
            'toolbar': attrs.get('toolbar', 'Full'),
            'height': attrs.get('height', '220'),
            'width': attrs.get('width', '765'),
        }
        rendered += mark_safe(u'<script type="text/javascript">'                                                \
                              u'   CKEDITOR.replace("%(name)s",'                                                \
                              u'       {'                                                                       \
                              u'           skin: "%(skin)s",'                                                   \
                              u'           toolbar: "%(toolbar)s",'                                             \
                              u'           height: "%(height)s",'                                               \
                              u'           width: "%(width)s",'                                                 \
                              u'       }'                                                                       \
                              u'   );'                                                                          \
                              u'</script>' % tokens)
        return rendered
