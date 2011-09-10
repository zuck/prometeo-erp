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

register = template.Library()

@register.simple_tag(takes_context=True)
def objects_from(context, obj):
    """
    Adds the "objects" variable to the context.

    Example tag usage: {% objects_from object %}
    """
    context['objects'] = obj.__class__._default_manager.all()
    return ''

@register.filter
def index_of(obj_list, obj):
    """
    Returns the index of an object in an object list.

    Example tag usage: {% object_list|index_of:object %}
    """
    return list(obj_list).index(obj)+1

@register.filter
def first_object(obj_list):
    """
    Returns the first object in an object list.

    Example tag usage: {% object_list|first_object %}
    """
    return obj_list[0]

@register.filter
def prev_object(obj_list, obj):
    """
    Returns the previous object in an object list.

    Example tag usage: {% object_list|prev_object:object %}
    """
    index = index_of(obj_list, obj)
    if index > 1:
        return obj_list[index-2]
    return obj

@register.filter
def next_object(obj_list, obj):
    """
    Returns the next object in an object list.

    Example tag usage: {% object_list|next_object:object %}
    """
    index = index_of(obj_list, obj)
    if index < obj_list.count():
        return obj_list[index]
    return obj

@register.filter
def last_object(obj_list):
    """
    Returns the last object in an object list.

    Example tag usage: {% object_list|last_object %}
    """
    return list(obj_list)[-1]
