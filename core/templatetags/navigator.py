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
from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist

from prometeo.core.templatetags import parse_args_kwargs

register = template.Library()

class ObjectsFromNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])
        
    def render_with_args(self, context, obj, filter_name="all", *args, **kwargs):
        method = getattr(obj.__class__._default_manager, filter_name)
        if callable(method):
            context['objects'] = method(*args, **kwargs)
        else:
            context['objects'] = method
        return ''
    
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
def objects_from(parser, token):
    """
    Adds the "objects" variable to the context.

    Example tag usages:

    {% objects_from object %}

    {% objects_from object "custom_filter" arg1 arg2 %}
    """
    tag_name, args, kwargs = parse_args_kwargs(parser, token)

    return ObjectsFromNode(*args, **kwargs)

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
