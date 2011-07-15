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

import re

from django import template
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string

from ..models import Menu

register = template.Library()

class MenuNode(template.Node):
    def __init__(self, slug, html_template):
        self.slug = slug
        self.html_template = html_template

    def render(self, context):
        output = ''
        slug = self.slug.resolve(context)
        try:
            menu = Menu.objects.get(slug=slug)
        except Menu.DoesNotExist:
            menu = None
        if isinstance(self.html_template, template.Variable):
            html_template = self.html_template.resolve(context)
        else:
            html_template = self.html_template
        if menu:
            output += render_to_string(html_template, { 'menu': menu }, context)
        return output

@register.tag
def menu(parser, token):
    try:
        args = token.split_contents()
        if len(args) < 2:
            raise ValueError
        elif len(args) == 2:
            slug = parser.compile_filter(args[1])
            html_template = 'menus/menu.html'
        else:
            slug = parser.compile_filter(args[1])
            html_template = parser.compile_filter(args[2])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one or two arguments" % token.contents.split()[0]

    return MenuNode(slug, html_template)
