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

from django.http import HttpResponseRedirect
from django.views.generic import list_detail
from django.utils.translation import check_for_language, activate
from django.conf import settings

from prometeo.core.utils import filter_objects

def set_language(request, lang, next=None):
    """Sets the current language.
    """
    if not next:
        next = request.REQUEST.get('next', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    if lang and check_for_language(lang):
        if hasattr(request, 'session'):
            request.session['django_language'] = lang
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    activate(lang)
    return response

def filtered_list_detail(request, model_or_queryset, fields=[], exclude=[], page=0, paginate_by=10, **kwargs):
    """Returns a filtered list of given objects.
    """
    field_names, filter_fields, object_list = filter_objects(
        request,
        model_or_queryset,
        fields=fields,
        exclude=exclude
    )

    extra_context = kwargs.pop('extra_context', {})
    extra_context.update({
        'field_names': field_names,
        'filter_fields': filter_fields,
    })

    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context=extra_context,
        **kwargs
    )
