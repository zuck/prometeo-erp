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
from django.utils.translation import ugettext_lazy as _

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    user = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('user'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    date_due = models.DateTimeField(null=True, blank=True, verbose_name=_('date due'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))      

    class Meta:
        ordering = ('created', 'id')
        get_latest_by = 'created'

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('task_detail', (), {"id": self.pk})
