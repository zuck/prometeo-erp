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

from django.core.paginator import Paginator
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def paginate(context, object_list, paginate_by=10):
    """Allows pagination on arbitrary querysets.
    """
    request = context['request']

    paginator = Paginator(object_list, paginate_by)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        p = paginator.page(page)
    except:
        p = paginator.page(paginator.num_pages)

    context['paginator'] = paginator
    context['page_obj'] = p
    context['object_list'] = p.object_list
        
    return ""
