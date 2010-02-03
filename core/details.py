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
__version__ = '$Revision$'

from django.utils.translation import ugettext as _
from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe
from django.db import models
from django.db.models import fields

from paginator import paginate

def value_to_string(value):
    if isinstance(value, float):
        return '%.2f' % value
    elif isinstance(value, bool):
        if not value:
            return '<span class="no">%s</span>' % _('No')
        return '<span class="yes">%s</span>' % _('Yes')
    if not value:
        return '<span class="disabled">%s</span>' % _('empty')
    return value

def field_to_value(field, instance):
    if isinstance(field, fields.related.RelatedField):
        relationship = getattr(instance, field.name)
        try:
            return '<a href="%s">%s</a>' % (relationship.get_absolute_url(), relationship)
        except AttributeError:
            return relationship
    elif isinstance(field, fields.EmailField):
        email = field.value_from_object(instance)
        if email:
            return '<a href="mailto:%s">%s</a>' % (email, email)
    elif isinstance(field, fields.BooleanField):
        flag = field.value_from_object(instance)
        if flag == '0' or not flag:
            return False
        return True
    elif field.choices:
        return getattr(instance, 'get_%s_display' % field.name)()
    return field.value_from_object(instance)

class Details(StrAndUnicode):
    def __init__(self, fields=[]):
        self.__fields = fields

    def _html_output(self, output):
        return mark_safe(output)
        
    def add_field(self, name, value):
        self.__fields.append((name, value))
        
    def remove_field(self, index):
        if len(self.__fields) > index:
            del self.__fields[index]

    def as_dl(self):
        output = "<dl>\n"
        for (f, v) in self.__fields:
            output += "\t<dt>%s</dt><dd>%s</dd>\n" % (_(f.capitalize()), value_to_string(v))
        output += "</dl>\n"
        return self._html_output(output)

    def as_table(self, header=("field", "value")):
        output = u"<table>\n"
        if header is not None:
            output += u"<thead><td>%s</td><td>%s</td></thead>" % (_(header[0].capitalize()), _(header[1].capitalize()))
        for (f, v) in self.__fields:
            output += u"\t<tr><td>%s</td><td>%s</td></tr>\n" % (_(f.capitalize()), value_to_string(v))
        output += u"</table>\n"
        return self._html_output(output)

class ModelDetails(Details):
    def __init__(self, instance, fields=[], exclude=['id']):
        field_list = [f for f in instance._meta.fields if len(fields) == 0 or f.attname in fields]
        fields = [(f.verbose_name, field_to_value(f, instance)) for f in field_list if f.attname not in exclude]
        super(ModelDetails, self).__init__(fields)
        
class ListDetails(StrAndUnicode):
    def __init__(self, data=[]):
        self._header = []
        self._rows = []
        for field, rows in data:
            self._header.append(field)
            for i, value in enumerate(rows):
                if i >= len(self._rows):
                    self._rows.append([])
                self._rows[i].append(value)
        print self._rows

    def _html_output(self, output):
        return mark_safe(output)
        
    def as_table(self):
        output = '<p class="disabled">%s</p>' % _('empty')
        if len(self._rows) > 0:
            output = u"<table>\n"
            output += u"\t<thead>\n"
            for field in self._header:
                output += u"\t\t<td>%s</td>\n" % (_(field.capitalize()))
            output += u"\t</thead>\n"
            for row in self._rows:
                output += u"\t<tr>\n"
                for i, field in enumerate(self._header):
                    output += u"\t\t<td>%s</td>\n" % (value_to_string(row[i]))
                output += u"\t</tr>\n"
            output += u"</table>\n"
        return self._html_output(output)
        
class ModelListDetails(ListDetails):
    def __init__(self, queryset=[], fields=[], exclude=['id'], with_actions=True):
        data = []
        if len(queryset) > 0:
            meta = queryset[0]._meta
            field_list = [f for f in meta.fields if (len(fields) == 0 or f.attname in fields) and f.attname not in exclude]
            for f in field_list:
                rows = []
                for instance in queryset:
                    rows.append(field_to_value(f, instance))
                data.append((f.verbose_name, rows))
            if with_actions:
                rows = []
                for i in queryset:
                    pattern = '<ul class="actions">\n'
                    if hasattr(i, 'get_absolute_url') and i.get_absolute_url():
                        pattern += '\t<li><a class="view" href="%s">%s</a></li>\n' % (i.get_absolute_url(), _('View'))
                    if hasattr(i, 'get_edit_url') and i.get_edit_url():
                        pattern += '\t<li><a class="edit" href="%s">%s</a></li>\n' % (i.get_edit_url(), _('Edit'))
                    if hasattr(i, 'get_delete_url') and i.get_delete_url():
                        pattern += '\t<li><a class="delete" href="%s">%s</a></li>\n' % (i.get_delete_url(), _('Delete'))
                    pattern += '</ul>'
                    rows.append(pattern)
                data.append((_('Actions'), rows))
        super(ModelListDetails, self).__init__(data)
        
class ModelPaginatedListDetails(ModelListDetails):
    def __init__(self, request, queryset=[], fields=[], exclude=['id']):
        self.__pages = paginate(request, queryset)
        super(ModelPaginatedListDetails, self).__init__(self.__pages.object_list, fields, exclude)
        
    def as_table(self):
        output = super(ModelPaginatedListDetails, self).as_table()
        if len(self._rows) > 0:
            output += '<div class="paginator">\n'
            
            # Previous.
            output += '\t<span class="previous">'
            if self.__pages.has_previous():
                output += '<a href="?page=%s"><span>&laquo;</span></a>' % self.__pages.previous_page_number()
            else:
                output += '<span class="disabled">&laquo;</span>'
            output += '</span>\n'
            
            # Current.
            output += '\t<span class="current">%s</span>\n' % (_('Page %(number)d of %(num_pages)d') % {'number': self.__pages.number, 'num_pages': self.__pages.paginator.num_pages})
            
            # Next.
            output += '\t<span class="next">'
            if self.__pages.has_next():
                output += '<a href="?page=%s"><span>&raquo;</span></a>' % self.__pages.next_page_number()
            else:
                output += '<span class="disabled">&raquo;</span>'
            output += '</span>\n'
            
            output += '</div>'
        
        return self._html_output(output)
    
