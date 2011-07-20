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

from django import template
from django.utils.translation import ugettext as _
from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe
from django.db import models
from django.db.models import fields
from django.template.loader import render_to_string
from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist

from prometeo.core.templatetags import parse_args_kwargs

register = template.Library()

def value_to_string(value):
    output = value
    if isinstance(value, float):
        output = '%.2f' % value
    elif isinstance(value, bool):
        if not value:
            output = '<span class="no">%s</span>' % _('No')
        else:
            output = '<span class="yes">%s</span>' % _('Yes')
    elif not value:
        output = '<span class="disabled">%s</span>' % _('empty')
    return mark_safe(output)

def field_to_value(field, instance):
    if isinstance(field, fields.related.RelatedField):
        relationship = getattr(instance, field.name)
        try:
            return '<a href="%s">%s</a>' % (relationship.get_absolute_url(), relationship)
        except AttributeError:
            return relationship
    elif isinstance(field, fields.URLField):
        url = field.value_from_object(instance)
        if url:
            return '<a href="%s">%s</a>' % (url, url)
    elif isinstance(field, fields.EmailField):
        email = field.value_from_object(instance)
        if email:
            return '<a href="mailto:%s">%s</a>' % (email, email)
    elif field.choices:
        return getattr(instance, 'get_%s_display' % field.name)()
    elif isinstance(field, fields.BooleanField):
        flag = field.value_from_object(instance)
        if flag == '0' or not flag:
            return False
        return True
    return field.value_from_object(instance)
    
def is_visible(field, fields=[], exclude=[]):
    return (len(fields) == 0 or field in fields) and field not in exclude

class DetailTableNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])

    def render_with_args(self, context, object_list, fields=[], exclude=['id'], with_actions=False, *args):
        data = []
        if len(object_list) > 0:
            meta = object_list[0]._meta
            field_list = [f for f in meta.fields if is_visible(f.attname, fields, exclude)]
            for f in field_list:
                rows = []
                for instance in object_list:
                    rows.append(field_to_value(f, instance))
                data.append((f.verbose_name, rows))
            if with_actions:
                rows = []
                for i, instance in enumerate(object_list):
                    rows.append(self.actions_template(i, instance))
                data.append((_('actions'), rows))
        self._header = []
        self._rows = []
        for field, rows in data:
            self._header.append(field)
            for i, value in enumerate(rows):
                if i >= len(self._rows):
                    self._rows.append([])
                self._rows[i].append(value)
        return self.as_table()
    
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
        
    def add_field(self, name, value):
        self.__fields.append((name, value))
        
    def remove_field(self, index):
        if len(self.__fields) > index:
            del self.__fields[index]

    def as_table(self):
        output = '<p class="disabled">%s</p>' % _('empty')
        if len(self._rows) > 0:
            output = self.table_template()
            output += u'\t<thead>\n'
            for field in self._header:
                output += u'\t\t<td>%s</td>\n' % (_(field.capitalize()))
            output += u'\t</thead>\n'
            for i, row in enumerate(self._rows):
                output += self.row_template(row, i)
                for j, field in enumerate(self._header):
                    output += self.column_template(row, j)
                output += u'\t</tr>\n'
            output += u'</table>\n'
        return self._html_output(output)
        
    def table_template(self):
        return u'<table>\n'
        
    def row_template(self, row, index):
        if (index % 2) == 1:
            return u'\t<tr class="altrow">\n'
        return u'\t<tr>\n'
        
    def column_template(self, row, index):
        value = row[index]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return u'\t\t<td class="number">%s</td>\n' % value_to_string(value)
        return u'\t\t<td>%s</td>\n' % value_to_string(value)

    def actions_template(self, index, instance):
        pattern = '<ul class="actions">\n'
        if hasattr(instance, 'get_absolute_url') and instance.get_absolute_url():
            pattern += '\t<li><a class="view" href="%s"><span>%s</span></a></li>\n' % (instance.get_absolute_url(), _('View'))
        if hasattr(instance, 'get_edit_url') and instance.get_edit_url():
            pattern += '\t<li><a class="edit" href="%s"><span>%s</span></a></li>\n' % (instance.get_edit_url(), _('Edit'))
        if hasattr(instance, 'get_delete_url') and instance.get_delete_url():
            pattern += '\t<li><a class="delete" href="%s"><span>%s</span></a></li>\n' % (instance.get_delete_url(), _('Delete'))
        pattern += '</ul>'
        return pattern

    def _html_output(self, output):
        return mark_safe(output)

@register.tag
def detail_table(parser, token):
    """
    Renders an interactive table from an object list.

    Example tag usage: {% detail_table object_list [fields] [exclude] [with_actions] %}
    """
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return DetailTableNode(*args, **kwargs)
