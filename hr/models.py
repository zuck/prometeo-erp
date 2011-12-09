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

from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from prometeo.core.utils import field_to_string

class Timesheet(models.Model):
    """Timesheet model.
    """
    date = models.DateField(verbose_name=_('date'))
    employee = models.ForeignKey('partners.Contact', verbose_name=_('employee'))

    class Meta:
        ordering = ('-date',)
        get_latest_by = '-date'
        verbose_name = _('timesheet')
        verbose_name_plural = _('timesheets')

    def __unicode__(self):
        return u"%s" % _('TS')

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
    task = models.ForeignKey('todo.Task', null=True, blank=True, verbose_name=_('related to'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))

    class Meta:
        ordering = ('-timesheet__date', 'start_time')
        verbose_name = _('timesheet entry')
        verbose_name_plural = _('timesheet entries')

    def __unicode__(self):
        return _('%(start_time)s ~ %(end_time)s on %(date)s of %(user)s') % {
            'start_time': field_to_string(self._meta.get_field_by_name('start_time')[0], self),
            'end_time': field_to_string(self._meta.get_field_by_name('end_time')[0], self),
            'date': field_to_string(self.timesheet._meta.get_field_by_name('date')[0], self.timesheet),
            'user': self.timesheet.user
        }

    def working_hours(self):
        start = datetime.combine(self.timesheet.date, self.start_time)
        end = datetime.combine(self.timesheet.date, self.end_time)
        return (end - start).total_seconds() / 3600
