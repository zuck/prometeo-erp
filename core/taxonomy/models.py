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
from django.db.models import permalink
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

class Result(models.Model):
    """Query result model.
    """
    title = models.CharField(_('title'), max_length=100)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('result')
        verbose_name_plural = _('results')

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

class Tag(models.Model):
    """Tag model.
    """
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title
        
    def _occurences(self):
        object_list = []
        related_objects = self._meta.get_all_related_many_to_many_objects()
        for related in related_objects:
            if related.opts.installed:
                model = related.model
                for obj in model.objects.select_related().filter(tags__title=self.title):
                    object_list.append(obj)
        return object_list
    occurences = property(_occurences)

    @models.permalink
    def get_absolute_url(self):
        return ("tag_detail", (), {"slug": self.slug})
        
class Category(models.Model):
    """Category model.
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)
        
    def _occurences(self):
        object_list = []
        related_objects = self._meta.get_all_related_many_to_many_objects()
        for related in related_objects:
            if related.opts.installed:
                model = related.model
                for obj in model.objects.select_related().filter(categories__title=self.title):
                    object_list.append(obj)
        return object_list
    occurences = property(_occurences)

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ("category_detail", (), {"slug": self.slug})
