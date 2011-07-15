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

from django.db.models import Q

def search(request, model, fields=[], exclude=['id']):
    matches = []
    queryset = None
    
    search_fields = get_search_fields(request, model, fields, exclude)
    
    if request.method == 'POST':
        queryset = []
        for f, value in search_fields:
            if value is not None:
                queryset.append(Q(**{"%s__startswith" % f.attname: value}) | Q(**{"%s__endswith" % f.attname: value}))

    if (queryset is not None):
        matches = model.objects.filter(*queryset)
    else:
        matches = model.objects.all()
        
    return search_fields, matches
    
def get_search_fields(request, model, fields, exclude):
    search_fields = [(f, search_field_value(request, f)) for f in model._meta.fields if is_visible(f.attname, fields, exclude)]
    return search_fields

def is_visible(field, fields=[], exclude=[]):
    return (len(fields) == 0 or field in fields) and field not in exclude

def search_field_value(request, field):
    name = field.attname
    if request.POST.has_key("sub_%s" % name):
        return None
    elif request.POST.has_key(name):
        return request.POST[name]
    elif request.POST.has_key(u'search_field') and request.POST[u'search_field'] == name:
        return request.POST[u'search_query']
    return None
