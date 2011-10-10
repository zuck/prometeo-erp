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

import copy
import pprint
import re

from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist

from prometeo.core.templatetags import parse_args_kwargs

register = template.Library()

# Inspired by http://code.google.com/p/django-crumbs/

class AddCrumbNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])
        
    def render_with_args(self, context, crumb, url=None, *args):
        href = None
        if url:
            if '/' in url:
                href = url
            else:
                href = reverse(url, args=args)
        if not hasattr(context['request'], 'breadcrumbs'):
            context['request'].breadcrumbs = []
        context['request'].breadcrumbs.append((u'%s' % crumb, href))
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
def add_crumb(parser, token):
    """
    Add a crumb to the breadcrumb list.

    Example tag usage: {% add_crumb name [url] %}
    """
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return AddCrumbNode(*args, **kwargs)

@register.simple_tag(takes_context=True)
def remove_last_crumb(context):
    """
    Remove the last crumb from the breadcrumb list.

    Example tag usage: {% remove_last_crumb %}
    """
    context['request'].breadcrumbs.pop()
    return ""

@register.inclusion_tag('elements/breadcrumbs.html', takes_context=True)
def render_breadcrumbs(context):
    """
    Renders the stored list of breadcrumbs.

    Example tag usage: {% render_breadcrumbs %}
    """
    try:
        breadcrumbs = context['request'].breadcrumbs
    except AttributeError:
        breadcrumbs = None
    return {'breadcrumbs': breadcrumbs}
