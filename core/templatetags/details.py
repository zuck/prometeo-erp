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

from django.db import models
from django.db.models import fields
from django import template
from django.template.loader import render_to_string
from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template.defaultfilters import date, time, striptags, truncatewords
from django.utils.translation import ugettext as _
from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe
from django.conf import settings

from prometeo.core.templatetags import parse_args_kwargs

register = template.Library()

class DetailTableNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])
        self.object_list = []
        self.field_list = []

    def render_with_args(self, context, object_list, fields=[], exclude=[], *args):
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
            self.field_list = [f for f in meta.fields if self.is_visible(f.name, fields, exclude)]
            output = self.table_template()
            output += u'\t<thead>\n'
            for f in self.field_list:
                verbose_name = _(f.verbose_name)
                verbose_name = verbose_name[0].capitalize() + verbose_name[1:]
                if f.name in order_by:
                    verse = "-"
                    aclass = "asc"
                    if "-%s" % f.name in order_by:
                        verse = ""
                        aclass = "desc"
                    output += u'\t\t<td><a class="%s" href="%sorder_by=%s%s">%s</a></td>\n' % (aclass, url, verse, f.name, verbose_name)
                else:
                    output += u'\t\t<td><a href="%sorder_by=%s">%s</a></td>\n' % (url, f.name, verbose_name)
            if 'actions' not in exclude and self.has_actions(instance):
                output += u'\t\t<td class="actions"></td>\n'
            output += u'\t</thead>\n'
            for i, instance in enumerate(self.object_list):
                output += self.row_template(instance, i)
                for j, f in enumerate(self.field_list):
                    output += self.column_template(instance, j)
                if 'actions' not in exclude:
                    output += self.actions_template(instance)
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
        
    def table_template(self):
        return u'<table>\n'
        
    def row_template(self, instance, index):
        if (index % 2) == 1:
            return u'\t<tr class="altrow">\n'
        return u'\t<tr>\n'
        
    def column_template(self, instance, index):
        css = ''
        value = self.field_to_value(self.field_list[index], instance)
        if index == 0:
            value = u'<a href="%s">%s</a>' % (instance.get_absolute_url(), self.value_to_string(value))
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            css = u' class="number"'
        return u'\t\t<td%s>%s</td>\n' % (css, self.value_to_string(value))

    def actions_template(self, instance):
        actions = []
        try:
            actions.append(u'<span class="edit"><a href="%s">%s</a></span>' % (instance.get_edit_url(), _('Edit')))
        except AttributeError:
            pass
        try:
            actions.append(u'<span class="delete"><a href="%s">%s</a></span>' % (instance.get_delete_url(), _('Delete')))
        except AttributeError:
            pass
        if len(actions) > 0:
            return u'\t\t<td class="actions">%s</td>\n' % ' '.join(actions)
        return u''
    
    def value_to_string(self, value):
        output = value
        if isinstance(value, float):
            output = u'%.2f' % value
        elif isinstance(value, bool):
            if not value:
                output = u'<span class="no">%s</span>' % _('No')
            else:
                output = u'<span class="yes">%s</span>' % _('Yes')
        elif not value:
            output = u'<span class="disabled">%s</span>' % _('Empty')
        return mark_safe(output)

    def field_to_value(self, field, instance):
        value = field.value_from_object(instance)
        if field.primary_key:
            return u'#%s' % value
        elif isinstance(field, fields.related.RelatedField):
            relationship = getattr(instance, field.name)
            try:
                return '<a href="%s">%s</a>' % (relationship.get_absolute_url(), relationship)
            except AttributeError:
                return relationship
        elif isinstance(field, fields.DateTimeField):
            return date(value, settings.DATETIME_FORMAT)
        elif isinstance(field, fields.DateField):
            return date(value, settings.DATE_FORMAT)
        elif isinstance(field, fields.TimeField):
            return time(value, settings.TIME_FORMAT)
        elif isinstance(field, fields.URLField):
            return u'<a href="%s">%s</a>' % (value, value)
        elif isinstance(field, fields.EmailField):
            return u'<a href="mailto:%s">%s</a>' % (value, value)
        elif isinstance(field, fields.TextField):
            return truncatewords(striptags(value), 6)
        elif field.choices:
            return getattr(instance, 'get_%s_display' % field.name)()
        elif isinstance(field, fields.BooleanField):
            if value == '0' or not value:
                return False
            return True
        return value
        
    def is_visible(self, field, fields=[], exclude=[]):
        return (len(fields) == 0 or field in fields) and field not in exclude

    def has_actions(self, instance):
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

@register.tag
def detail_table(parser, token):
    """
    Renders an interactive table from an object list.

    Example tag usage: {% detail_table object_list [fields] [exclude] %}
    """
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return DetailTableNode(*args, **kwargs)
