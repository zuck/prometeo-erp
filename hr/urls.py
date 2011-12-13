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

urlpatterns = patterns('hr.views',

    # Timesheets.
    url(r'^timesheets/$', view='timesheets.timesheet_list', name='timesheet_list'),
    url(r'^timesheets/add/$', view='timesheets.timesheet_add', name='timesheet_add'),
    url(r'^timesheets/(?P<id>\d+)/$', view='timesheets.timesheet_detail', name='timesheet_detail'),
    url(r'^timesheets/(?P<id>\d+)/edit/$', view='timesheets.timesheet_edit', name='timesheet_edit'),
    url(r'^timesheets/(?P<id>\d+)/delete/$', view='timesheets.timesheet_delete', name='timesheet_delete'),
    url(r'^timesheets/(?P<id>\d+)/timeline/$', 'timesheets.timesheet_detail', {'template_name': 'hr/timesheet_timeline.html'}, 'timesheet_timeline'),
    url(r'^timesheets/(?P<id>\d+)/hard-copies/$', view='timesheets.timesheet_hardcopies', name='timesheet_hardcopies'),
    url(r'^timesheets/(?P<id>\d+)/hard-copies/add/$', view='timesheets.timesheet_add_hardcopy', name='timesheet_add_hardcopy'),

    # Expense vouchers.
    url(r'^expensevouchers/$', view='expensevouchers.expensevoucher_list', name='expensevoucher_list'),
    url(r'^expensevouchers/add/$', view='expensevouchers.expensevoucher_add', name='expensevoucher_add'),
    url(r'^expensevouchers/(?P<id>\d+)/$', view='expensevouchers.expensevoucher_detail', name='expensevoucher_detail'),
    url(r'^expensevouchers/(?P<id>\d+)/edit/$', view='expensevouchers.expensevoucher_edit', name='expensevoucher_edit'),
    url(r'^expensevouchers/(?P<id>\d+)/delete/$', view='expensevouchers.expensevoucher_delete', name='expensevoucher_delete'),
    url(r'^expensevouchers/(?P<id>\d+)/timeline/$', 'expensevouchers.expensevoucher_detail', {'template_name': 'hr/expensevoucher_timeline.html'}, 'expensevoucher_timeline'),
    url(r'^expensevouchers/(?P<id>\d+)/hard-copies/$', view='expensevouchers.expensevoucher_hardcopies', name='expensevoucher_hardcopies'),
    url(r'^expensevouchers/(?P<id>\d+)/hard-copies/add/$', view='expensevouchers.expensevoucher_add_hardcopy', name='expensevoucher_add_hardcopy'),
)
