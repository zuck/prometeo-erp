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

import datetime

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from prometeo.core.models import Commentable

class Event(Commentable):
    """Event model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    start = models.DateTimeField(null=True, blank=True, verbose_name=_('start'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end'))
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('location'))
    status = models.CharField(max_length=100, choices=settings.EVENT_STATUS_CHOICES, default=settings.EVENT_DEFAULT_STATUS, verbose_name=_('status'))
    attendees = models.ManyToManyField('auth.User', null=True, blank=True, verbose_name=_('attendees'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    author = models.ForeignKey('auth.User', related_name='created_events', null=True, blank=True, verbose_name=_('author'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_("stream"))

    class Meta:
        ordering = ('-start', 'id')
        get_latest_by = '-start'

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
