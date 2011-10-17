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

from django.conf.urls.defaults import *

urlpatterns = patterns('todo.views',

    # Tasks.
    url(r'^tasks/$', view='task_list', name='task_list'),
    url(r'^tasks/unplanned/$', view='unplanned_task_list', name='unplanned_task_list'),
    url(r'^tasks/add/$', view='task_add', name='task_add'),
    url(r'^tasks/(?P<id>\d+)/$', view='task_detail', name='task_detail'),
    url(r'^tasks/(?P<id>\d+)/edit/$', view='task_edit', name='task_edit'),
    url(r'^tasks/(?P<id>\d+)/delete/$', view='task_delete', name='task_delete'),
    url(r'^tasks/(?P<id>\d+)/close/$', view='task_close', name='task_close'),
    url(r'^tasks/(?P<id>\d+)/reopen/$', view='task_reopen', name='task_reopen'),

    # Timesheets.
    url(r'^tasks/timesheets/$', view='timesheet_list', name='timesheet_list'),
    url(r'^tasks/timesheets/add/$', view='timesheet_add', name='timesheet_add'),
    url(r'^tasks/timesheets/(?P<id>\d+)/$', view='timesheet_detail', name='timesheet_detail'),
    url(r'^tasks/timesheets/(?P<id>\d+)/edit/$', view='timesheet_edit', name='timesheet_edit'),
    url(r'^tasks/timesheets/(?P<id>\d+)/delete/$', view='timesheet_delete', name='timesheet_delete'),
)
