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

import datetime

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from prometeo.core.models import Commentable

from managers import *

class Event(Commentable):
    """Event model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    start = models.DateTimeField(verbose_name=_('start date'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end date'))
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('location'))
    status = models.CharField(max_length=100, choices=settings.EVENT_STATUS_CHOICES, default=settings.EVENT_DEFAULT_STATUS, verbose_name=_('status'))
    attendees = models.ManyToManyField('auth.User', null=True, blank=True, verbose_name=_('attendees'))
    public = models.BooleanField(default=False, verbose_name=_('public?'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    author = models.ForeignKey('auth.User', related_name='created_events', null=True, blank=True, verbose_name=_('created by'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    objects = EventManager()

    class Meta:
        ordering = ('-start', 'id')
        get_latest_by = '-start'
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('event_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('event_delete', (), {"id": self.pk})

    def save(self):
        if self.start and not self.end:
            self.end = self.start + datetime.timedelta(hours=1)
        super(Event, self).save()
