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

from django.db import models
from django.db.models import Q, query
from django.db.models import fields as django_fields
from django.utils.encoding import StrAndUnicode
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template.defaultfilters import date, time, striptags, truncatewords
from django.conf import settings

def clean_referer(request, default_referer='/'):
    """Returns the HTTP referer of the given <request>.
    
    If the HTTP referer is not recognizable, <default_referer> is returned.
    """
    referer = request.META.get('HTTP_REFERER', default_referer)
    return referer.replace("http://", "").replace(request.META['HTTP_HOST'], "")

def value_to_string(value):
    """Tries to return a smart string representation of the given <value>.
    """
    output = value
    if isinstance(value, (list, tuple)):
        output = ', '.join(value)
    elif isinstance(value, bool):
        if not value:
            output = u'<span class="no">%s</span>' % _('No')
        else:
            output = u'<span class="yes">%s</span>' % _('Yes')
    elif isinstance(value, float):
        output = u'%.2f' % value
    elif isinstance(value, int):
        output = '%d' % value
    if not value and not output:
        output = u'<span class="disabled">%s</span>' % _('empty')
    return mark_safe(output)

def field_to_value(field, instance):
    """Tries to convert a model field value in something smarter to render.
    """
    value = getattr(instance, field.name)
    if field.primary_key:
        return u'#%s' % value
    elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
        try:
            return '<a href="%s">%s</a>' % (value.get_absolute_url(), value)
        except AttributeError:
            return value
    elif isinstance(field, models.ManyToManyField):
        items = []
        for item in value.all():
            try:
                items.append('<a href="%s">%s</a>' % (item.get_absolute_url(), item))
            except AttributeError:
                items.append(item)
        return items
    elif isinstance(field, models.DateTimeField):
        return date(value, settings.DATETIME_FORMAT)
    elif isinstance(field, models.DateField):
        return date(value, settings.DATE_FORMAT)
    elif isinstance(field, models.TimeField):
        return time(value, settings.TIME_FORMAT)
    elif isinstance(field, models.URLField) and value:
        return u'<a href="%s">%s</a>' % (value, value)
    elif isinstance(field, models.EmailField) and value:
        return u'<a href="mailto:%s">%s</a>' % (value, value)
    elif field.choices:
        return getattr(instance, 'get_%s_display' % field.name)()
    elif isinstance(field, models.BooleanField):
        if value == '0' or not value:
            return False
        return True
    return value

def field_to_string(field, instance):
    """All-in-one conversion from a model field value to a smart string representation.
    """
    return value_to_string(field_to_value(field, instance))

def is_visible(field_name, fields=[], exclude=[]):
    """Checks if <field_name> is in the resulting combination of <fields> and <exclude>.
    """
    return (len(fields) == 0 or field_name in fields) and field_name not in exclude

def filter_field_value(request, field):
    """Retrieves from POST the value of the filter related to the given <field>.
    """
    name = field.name
    if request.POST.has_key("sub_%s" % name):
        return None
    elif request.POST.has_key(name):
        return request.POST[name]
    elif request.POST.has_key(u'filter_field') and request.POST[u'filter_field'] == name:
        return request.POST[u'filter_query']
    return None
    
def get_filter_fields(request, model, fields, exclude):
    """Returns the list of available filters for the given <model>.
    """
    return [(f, filter_field_value(request, f)) for f in model._meta.fields if is_visible(f.name, fields, exclude)]

def filter_objects(request, model_or_queryset=None, fields=[], exclude=[]):
    """Returns a queryset of filtered objects.

    <model_or_queryset> can be a Model class or a starting queryset.
    """
    matches = []
    model = None
    object_list = None
    queryset = None

    if isinstance(model_or_queryset, query.QuerySet):
        model = model_or_queryset.model
        object_list = model_or_queryset

    elif issubclass(model_or_queryset, models.Model):
        model = model_or_queryset
        object_list = model.objects.all()

    if not object_list.query.can_filter():
        pks = [instance.pk for instance in object_list]
        object_list = model.objects.filter(pk__in=pks)
    
    filter_fields = get_filter_fields(request, model, fields, exclude)
    
    if request.method == 'POST':
        queryset = []
        for f, value in filter_fields:
            if value is not None:
                if isinstance(f, django_fields.related.RelatedField):
                    pass # Fail silently.
                else:
                    queryset.append(Q(**{"%s__startswith" % f.name: value}) | Q(**{"%s__endswith" % f.name: value}))

    if (queryset is not None):
        matches = object_list.filter(*queryset)
    else:
        matches = object_list

    try:
        order_by = request.GET['order_by']
        matches = matches.order_by(order_by)
    except:
        pass
        
    return [f.name for f, value in filter_fields], SortedDict(filter_fields), matches
