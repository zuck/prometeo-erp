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
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import *
from django.utils.translation import ugettext_lazy as _

class Observable(object):
    """Mix-in that sends a special signal when a field is changed.
    """
    def __init__(self, *args, **kwargs):
        super(Observable, self).__init__(*args, **kwargs)
        self.__changes = {}

    def __setattr__(self, name, value):
        try:
            if self.pk and name != 'modified' and name in [f.attname for f in self._meta.fields]:
                old_value = getattr(self, name)
                if name in self.__changes:
                    old_value = self.__changes[name][0]
                if value != old_value:
                    self.__changes[name] = (old_value, value)
        except AttributeError:
            pass
        super(Observable, self).__setattr__(name, value)

class Stream(models.Model):
    """Stream model.
    """
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    followers = models.ManyToManyField('auth.User', null=True, verbose_name=_('followers'))
    
    class Meta:
        verbose_name = _('stream')
        verbose_name_plural = _('streams')

    def __unicode__(self):
        return self.slug

class Activity(models.Model):
    """Activity model.
    """
    actor_content_type = models.ForeignKey(ContentType, related_name='actor')
    actor_object_id = models.PositiveIntegerField()
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')
    action = models.CharField(max_length=255, verbose_name=_('action'))
    target_content_type = models.ForeignKey(ContentType, related_name='target', blank=True, null=True)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    streams = models.ManyToManyField(Stream, null=True, verbose_name=_('streams'))
    backlink = models.CharField(_('backlink'), blank=True, null=True, max_length=200)
    
    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ('-created',)

    def __unicode__(self):
        if self.target_content_type:
            if self.target:
                return _(u'%s %s %s %s') % (self.actor, self.action, self.target_content_type, self.target)
            else:
                return _(u'%s %s %s') % (self.actor, self.action, self.target_content_type)
        return _(u'%s %s') % (self.actor, self.action)

    def signature(self):
        """Signature of this activity.
        """
        if self.target_content_type:
            return "%s-%s-%s" % (self.actor_content_type.name, self.action, self.target_content_type.name)
        return "%s-%s" % (self.actor_content_type.name, self.action)

    def get_absolute_url(self):
        if self.backlink:
            return self.backlink
        try:
            return self.target.get_absolute_url()
        except:
            pass
        try:
            return self.actor.get_absolute_url()
        except:
            pass
        return ""
