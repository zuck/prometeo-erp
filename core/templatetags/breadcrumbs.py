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

# Inspired by http://code.google.com/p/django-crumbs/

import copy
import pprint
import re

from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist

register = template.Library()

def parse_args_kwargs(parser, token):
    contents = token.split_contents()
    tag_name = contents[0]
    args_list = contents[1:]
    args = []
    kwargs = {}
    
    for value in args_list:
        if '=' in value:
            k, v = value.split('=', 1)
            kwargs[str(k)] = v
        else:
            args.append(value)
    
    return tag_name, args, kwargs

class CaktNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])
        
    def render_with_args(self, context, *args, **kwargs):
        raise Exception('render_with_args must be implemented the class that inherits CaktNode')
    
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

class AddCrumbNode(CaktNode):
    def render_with_args(self, context, crumb, url=None, *args):
        href = None
        if url:
            if '/' in url:
                href = url
            else:
                href = reverse(url, args=args)
        if not hasattr(context['request'], 'breadcrumbs'):
            context['request'].breadcrumbs = []
        context['request'].breadcrumbs.append((crumb, href))
        return ''

@register.tag
def add_crumb(parser, token):
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return AddCrumbNode(*args, **kwargs)

@register.inclusion_tag('breadcrumbs/breadcrumbs.html', takes_context=True)
def render_breadcrumbs(context):
    try:
        breadcrumbs = context['request'].breadcrumbs
    except AttributeError:
        breadcrumbs = None
    return {'breadcrumbs': breadcrumbs}
