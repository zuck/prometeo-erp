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

from django import template

from prometeo.core.utils import filter_objects

register = template.Library()

@register.simple_tag(takes_context=True)
def filter_by(context, object_list, fields=[], exclude=[], template_object_name="object"):
    """Allows filtering of arbitrary models.
    """
    request = context['request']

    field_names, filter_fields, filtered_object_list = filter_objects(request, object_list, fields, exclude)

    context['filter_field_names'] = field_names
    context['filter_fields'] = filter_fields
    context[u'%s_list' % template_object_name] = filtered_object_list

    return ""
