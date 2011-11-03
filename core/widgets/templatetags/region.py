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

import re

from django import template
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

from ..models import Region
from widget import WidgetNode

register = template.Library()

class RegionNode(template.Node):
    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        output = ''
        slug = self.slug.resolve(context)
        try:
            region = Region.objects.get(slug=slug)
        except Region.DoesNotExist:
            region = None
        if region:
            for index, widget in enumerate(region.widgets.all()):
                context['widget_index'] = index
                output += WidgetNode(widget.slug).render(context)
        return output

@register.tag
def region(parser, token):
    region_name = ''
    try:
        args = token.split_contents()
        if len(args) == 2:
            region_name = parser.compile_filter(args[1])
        else:
            raise ValueError
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    return RegionNode(region_name)
