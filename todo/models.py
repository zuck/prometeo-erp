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

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

from managers import *

class Task(models.Model):
    """Task model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    user = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('user'))
    start = models.DateTimeField(null=True, blank=True, verbose_name=_('start'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on')) 
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))

    objects = TaskManager() 

    class Meta:
        ordering = ('-start', 'id')
        get_latest_by = '-start'

    def __unicode__(self):
        return u'%s' % self.title

    def planned(self):
        return (self.start is not None)

    def started(self):
        return (self.start <= datetime.now())

    def expired(self):
        return (self.end < datetime.now())

    @models.permalink
    def get_absolute_url(self):
        return ('task_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('task_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('task_delete', (), {"id": self.pk})
