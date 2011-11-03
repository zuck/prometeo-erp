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

from datetime import datetime, timedelta

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from prometeo.core.utils import field_to_string, value_to_string

from managers import *

class Task(models.Model):
    """Task model.
    """
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    user = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('owner'))
    start = models.DateTimeField(null=True, blank=True, verbose_name=_('start date'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end date'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))

    objects = TaskManager()

    class Meta:
        ordering = ('-start',)
        get_latest_by = '-start'
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('task_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('task_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('task_delete', (), {"id": self.pk})

    def save(self):
        if self.start and not self.end:
            self.end = self.start + timedelta(hours=1)
        super(Task, self).save()

    def planned(self):
        return (self.start is not None)

    def started(self):
        return (self.start <= datetime.now())

    def expired(self):
        return (self.end < datetime.now())

    def working_hours(self):
        count = 0
        entries = self.timesheetentry_set.all()
        if entries:
            for entry in self.timesheetentry_set.all():
                count += entry.working_hours()
        elif self.planned():
            count = (self.end - self.start).total_seconds() / 3600 
        return count

class Timesheet(models.Model):
    """Timesheet model.
    """
    date = models.DateField(verbose_name=_('date'))
    user = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('owner'))
    status = models.CharField(max_length=10, choices=settings.TIMESHEET_STATUS_CHOICES, default=settings.TIMESHEET_DEFAULT_STATUS, verbose_name=_('status'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))

    class Meta:
        ordering = ('-date',)
        get_latest_by = '-date'
        verbose_name = _('timesheet')
        verbose_name_plural = _('timesheets')

    def __unicode__(self):
        return _('Timesheet of %s') % field_to_string(self._meta.get_field_by_name('date')[0], self)

    @models.permalink
    def get_absolute_url(self):
        return ('timesheet_detail', (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ('timesheet_edit', (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('timesheet_delete', (), {"id": self.pk})

    def working_hours(self):
        count = 0
        for entry in self.entries.all():
            count += entry.working_hours()
        return count

class TimesheetEntry(models.Model):
    """Timesheet entry model.
    """
    timesheet = models.ForeignKey(Timesheet, related_name='entries', verbose_name=_('timesheet'))
    start_time = models.TimeField(verbose_name=_('start time'))
    end_time = models.TimeField(verbose_name=_('end time'))
    task = models.ForeignKey(Task, null=True, blank=True, verbose_name=_('related to'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))

    class Meta:
        ordering = ('-timesheet__date', 'start_time')
        verbose_name = _('timesheet entry')
        verbose_name_plural = _('timesheet entries')

    def __unicode__(self):
        return _('%s ~ %s on %s of %s') % (
            field_to_string(self._meta.get_field_by_name('start_time')[0], self),
            field_to_string(self._meta.get_field_by_name('end_time')[0], self),
            field_to_string(self.timesheet._meta.get_field_by_name('date')[0], self.timesheet),
            self.timesheet.user
        )

    def working_hours(self):
        start = datetime.combine(self.timesheet.date, self.start_time)
        end = datetime.combine(self.timesheet.date, self.end_time)
        return (end - start).total_seconds() / 3600
