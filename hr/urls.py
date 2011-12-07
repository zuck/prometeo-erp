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

from django.conf.urls.defaults import *

urlpatterns = patterns('',

    # Timesheets.
    url(r'^timesheets/$', view='hr.views.timesheet_list', name='timesheet_list'),
    url(r'^timesheets/add/$', view='hr.views.timesheet_add', name='timesheet_add'),
    url(r'^timesheets/(?P<id>\d+)/$', view='hr.views.timesheet_detail', name='timesheet_detail'),
    url(r'^timesheets/(?P<id>\d+)/edit/$', view='hr.views.timesheet_edit', name='timesheet_edit'),
    url(r'^timesheets/(?P<id>\d+)/delete/$', view='hr.views.timesheet_delete', name='timesheet_delete'),
    url(r'^timesheets/(?P<id>\d+)/timeline/$', 'hr.views.timesheet_detail', {'template_name': 'hr/timesheet_timeline.html'}, 'timesheet_timeline'),
    url(r'^timesheets/(?P<id>\d+)/hard-copies/$', view='documents.views.hardcopy_list', name='timesheet_hardcopies'),
    url(r'^timesheets/(?P<id>\d+)/hard-copies/add/$', view='documents.views.hardcopy_add', name='timesheet_add_hardcopy'),
)
