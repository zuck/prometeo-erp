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
from django.db.models.fields import related

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
            output += "\t<dt>%s</dt><dd>%s</dd>\n" % (f.capitalize(), self._value_or_empty(v))
        output += "</dl>\n"
        return self._html_output(output)

    def as_table(self, header=("field", "value")):
        output = u"<table>\n"
        if header is not None:
            output += u"<thead><td>%s</td><td>%s</td></thead>" % (header[0].capitalize(), header[1].capitalize())
        for (f, v) in self.__fields:
            output += u"\t<tr><td>%s</td><td>%s</td></tr>\n" % (f.capitalize(), self._value_or_empty(v))
        output += u"</table>\n"
        return self._html_output(output)

    def _value_or_empty(self, value):
        if isinstance(value, float):
            return '%.2f' % value
        if not value:
            return "<span class=\"disabled\">empty</span>"
        return value

class ModelDetails(Details):
    def __init__(self, instance, fields=[], exclude=['id']):
        self.__instance = instance
        field_list = [f for f in self.__instance._meta.fields if len(fields) == 0 or f.attname in fields]
        fields = [(f.verbose_name, self._value_to_string(f)) for f in field_list if f.attname not in exclude]
        super(ModelDetails, self).__init__(fields)

    def _value_to_string(self, field):
        if isinstance(field, related.RelatedField):
            relationship = getattr(self.__instance, field.name)
            try:
                return '<a href="%s">%s</a>' % (relationship.get_absolute_url(), relationship)
            except AttributeError:
                return relationship
        elif isinstance(field, models.fields.FloatField):
            return '%.2f' % field.value_from_object(self.__instance)
        elif field.choices:
            return getattr(self.__instance, 'get_%s_display' % field.name)()
        elif isinstance(field, models.BooleanField):
            flag = field.value_to_string(self.__instance)
            if flag == '0':
                return '<span class="no">%s</span>' % _('No')
            return '<span class="yes">%s</span>' % _('Yes')
        return field.value_to_string(self.__instance)
