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

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class GFKQuerySet(QuerySet):
    def filter(self, **kwargs):
        gfk_fields = [g for g in self.model._meta.virtual_fields if isinstance(g, GenericForeignKey)]

        for gfk in gfk_fields:
            if kwargs.has_key(gfk.name):
                param = kwargs.pop(gfk.name)
                kwargs[gfk.fk_field] = param.pk
                kwargs[gfk.ct_field] = ContentType.objects.get_for_model(param)

        return super(GFKQuerySet, self).filter(**kwargs)

class GFKManager(models.Manager):
    def get_query_set(self):
        return GFKQuerySet(self.model)

class NotificationQuerySet(GFKQuerySet):
    def read(self):
        return self.filter(read__isnull=False)

    def unread(self):
        return self.filter(read__isnull=True)

    def for_object(self, instance):
        return self.filter(target=instance)
        
    def read_for_object(self, instance):
        return self.for_object(instance).filter(read__isnull=False)

    def unread_for_object(self, instance):
        return self.for_object(instance).filter(read__isnull=True)

class NotificationManager(GFKManager):
    """Manager for notifications.
    """
    def get_query_set(self):
        return NotificationQuerySet(self.model)

    def read(self):
        return self.get_query_set().read()

    def unread(self):
        return self.get_query_set().unread()

    def for_object(self, instance):
        return self.get_query_set().for_object(instance)
        
    def read_for_object(self, instance):
        return self.get_query_set().read_for_object(instance)

    def unread_for_object(self, instance):
        return self.get_query_set().unread_for_object(instance)
