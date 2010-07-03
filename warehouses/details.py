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

from django.utils.translation import ugettext_lazy as _

from prometeo.core import details

class WarehouseListDetails(details.ModelPaginatedListDetails):
    def __init__(self, request, queryset=[], fields=[], exclude=['id'], with_actions=True):
        super(WarehouseListDetails, self).__init__(request, queryset, fields, exclude, with_actions)
        if 'value' not in exclude:
            self._header.insert(-1, _('value'))
            for i, instance in enumerate(queryset):
                self._rows[i].insert(-1, instance.value())

class MovementListDetails(details.ModelPaginatedListDetails):
    def __init__(self, request, queryset=[], fields=[], exclude=['id'], with_actions=True):
        super(MovementListDetails, self).__init__(request, queryset, fields, exclude, with_actions)
        if 'value' not in exclude:
            self._header.insert(-2, _('value'))
            for i, instance in enumerate(queryset):
                self._rows[i].insert(-2, instance.value())
            
    def row_template(self, row, index):
        i = self._header.index(_('verse'))
        value = details.value_to_string(row[i])
        if value == _('income'):
            return u'\t<tr class="in">\n'
        return u'\t<tr class="out">\n'
        
    def column_template(self, row, index):
        i = self._header.index(_('verse'))
        if index == i:
            value = row[index]
            return u'\t\t<td class="verse">%s</td>\n' % details.value_to_string(value)
        return super(MovementListDetails, self).column_template(row, index)
