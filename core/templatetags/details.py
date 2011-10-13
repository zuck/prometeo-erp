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

import pickle

from django.db import models
from django import forms
from django.forms.forms import BoundField
from django.forms.util import flatatt
from django import template
from django.template.loader import render_to_string
from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from prometeo.core.templatetags import parse_args_kwargs
from prometeo.core.utils import is_visible, value_to_string, field_to_value

register = template.Library()
        
def row_template(index):
    if (index % 2) == 1:
        return u'\t<tr class="altrow">\n'
    return u'\t<tr>\n'

def field_template(name, field, form_or_model, attrs={'colspan': "3"}):
    label = ""
    value = ""
    output = ""
    td_attrs = {}

    if isinstance(field, models.Field):
        label = u'%s' % field.verbose_name
        value = value_to_string(field_to_value(field, form_or_model))

    elif isinstance(field, forms.Field):
        bf = BoundField(form_or_model, field, name)
        label = u'%s' % bf.label_tag()
        value = u'%s' % bf
        if bf.help_text:
            value += '<br/>\n<span class="help_text">%s</span>' % (u'%s' % bf.help_text)
        if bf._errors():
            value += '<br/>\n<ul class="errorlist">\n'
            for error in bf._errors():
                value += '\t<li>%s</li>\n' % error
            value += '</ul>\n'
        css_classes = bf.css_classes()
        if css_classes:
            td_attrs['class'] = css_classes

    else:
        label = u'%s' % name
        value = value_to_string(field)
    
    td_attrs.update(attrs)

    if label and value:
        output += ("\t\t<th>%s</th>\n" % (label[0].capitalize() + label[1:]))
        output += "\t\t<td%s>\n" % flatatt(td_attrs)
        output += "\t\t\t%s\n" % value
        output += "\t\t</td>\n"

    return output

def actions_template(instance):
    actions = []
    try:
        actions.append(u'<span class="edit"><a href="%s">%s</a></span>' % (instance.get_edit_url(), _('Edit')))
    except AttributeError:
        pass
    try:
        actions.append(u'<span class="delete"><a href="%s">%s</a></span>' % (instance.get_delete_url(), _('Delete')))
    except AttributeError:
        pass
    output = ' '.join(actions)
    if output:
        output = u'<span class="actions">%s</span>' % output
    return output

def has_actions(instance):
    actions = 0
    try:
        instance.get_edit_url()
        actions += 1
    except AttributeError:
        pass
    try:
        instance.get_delete_url()
        actions += 1
    except AttributeError:
        pass
    return (actions > 0)

class DetailTableNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])
        self.object_list = []
        self.field_list = []

    def render_with_args(self, context, object_list, fields=[], exclude=[], *args, **kwargs):
        self.object_list = object_list
        request = context['request']
        url = './?' + ''.join(['%s=%s&' % (key, value) for key, value in request.GET.items() if key != "order_by"])
        try:
            order_by = request.GET['order_by']
        except:
            order_by = []
        output = '<p class="disabled">%s</p>' % _('No results found.')
        if len(self.object_list) > 0:
            instance = self.object_list[0]
            meta = instance._meta
            self.field_list = [f for f in meta.fields if is_visible(f.name, fields, exclude)]
            output = u'<table>\n'
            output += u'\t<tr>\n'
            for f in self.field_list:
                verbose_name = _(f.verbose_name)
                verbose_name = verbose_name[0].capitalize() + verbose_name[1:]
                field_type = f.__class__.__name__.lower().replace("field", "")
                if f.choices:
                    field_type += "_choices"
                if f.name in order_by:
                    verse = "-"
                    aclass = "asc"
                    if "-%s" % f.name in order_by:
                        verse = ""
                        aclass = "desc"
                    output += u'\t\t<th class="%s"><a class="%s" href="%sorder_by=%s%s">%s</a></th>\n' % (field_type, aclass, url, verse, f.name, verbose_name)
                else:
                    output += u'\t\t<th class="%s"><a href="%sorder_by=%s">%s</a></th>\n' % (field_type, url, f.name, verbose_name)
            output += u'\t</tr>\n'
            for i, instance in enumerate(self.object_list):
                output += row_template(i)
                for j, f in enumerate(self.field_list):
                    output += self.column_template(instance, j, ('actions' not in exclude))
                output += u'\t</tr>\n'
            output += u'</table>\n'
        return mark_safe(output)
    
    def render(self, context):
        args = []
        for arg in self.args:
            try:
                args.append(arg.resolve(context)) 
            except VariableDoesNotExist:
                args.append(None)
        
        kwargs = {}
        for k, arg in self.kwargs.items():
            try:
                kwargs[k] = arg.resolve(context)
            except VariableDoesNotExist:
                kwargs[k] = None
        
        return self.render_with_args(context, *args, **kwargs)
        
    def column_template(self, instance, index, with_actions=True):
        css = ''
        value = field_to_value(self.field_list[index], instance)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            css = u' class="number"'
        value = value_to_string(value)
        if index == 0 and hasattr(instance, 'get_absolute_url'):
            value = u'<a href="%s">%s</a>' % (instance.get_absolute_url(), value)
        elif index == len(self.field_list)-1 and with_actions:
            value += " " + actions_template(instance)
        return u'\t\t<td%s>%s</td>\n' % (css, value)

@register.tag
def detail_table(parser, token):
    """Renders an interactive table from an object list.

    Example tag usage: {% detail_table object_list [fields] [exclude] %}
    """
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return DetailTableNode(*args, **kwargs)

class PropertyTableNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])

    def render_with_args(self, context, form_or_instance, layout=None, *args, **kwargs):
        output = ""

        if isinstance(form_or_instance, (models.Model, forms.ModelForm)):
            fields = {}
            output = '<table class="properties">\n'
            
            if isinstance(form_or_instance, models.Model):
                fields = dict([(f.name, f) for f in (form_or_instance._meta.fields + form_or_instance._meta.many_to_many)])
            else:
                fields = form_or_instance.fields

            if layout is None:
                layout = [n for n, f in fields.items()]
            elif isinstance(layout, basestring):
                layout = eval(layout)
            else:
                return ""

            for i, field in enumerate(layout):
                output += row_template(i)

                # Single field.
                if isinstance(field, basestring):
                    name = field
                    if field in fields:
                        field = fields[name]
                    else:
                        field = getattr(form_or_instance, name)
                    output += field_template(name, field, form_or_instance)

                # Many fields on the same row.
                elif isinstance(field, list):
                    for i, f in enumerate(field):
                        if isinstance(f, basestring):
                            name = f
                            if f in fields:
                                f = fields[name]
                            else:
                                f = getattr(form_or_instance, name)
                            output += field_template(name, f, form_or_instance, {})

                output += '\t</tr>\n'

            output += '</table>\n'

        return mark_safe(output)
    
    def render(self, context):
        args = []
        for arg in self.args:
            try:
                args.append(arg.resolve(context)) 
            except VariableDoesNotExist:
                args.append(None)
        
        kwargs = {}
        for k, arg in self.kwargs.items():
            try:
                kwargs[k] = arg.resolve(context)
            except VariableDoesNotExist:
                kwargs[k] = None
        
        return self.render_with_args(context, *args, **kwargs)

@register.tag
def property_table(parser, token):
    """Renders a property table from a ModelForm or an object instance.

    Example tag usage: {% property_table form [field1, [field2, field3], field4] %}
    """
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return PropertyTableNode(*args, **kwargs)
