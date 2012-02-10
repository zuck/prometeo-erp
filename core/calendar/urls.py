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

urlpatterns = patterns('prometeo.core.calendar.views',

    url(r'^events/$', view='event_list', name='event_list'),
    url(r'^events/day/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', view='event_day', name='event_day'),
    url(r'^events/week/(?P<year>\d+)/(?P<week>\d+)/$', view='event_week', name='event_week'),
    url(r'^events/month/(?P<year>\d+)/(?P<month>\d+)/$', view='event_month', name='event_month'),
    url(r'^events/year/(?P<year>\d+)/$', view='event_year', name='event_year'),
    url(r'^events/add/$', view='event_add', name='event_add'),
    url(r'^events/add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', view='event_add', name='event_add_with_date'),
    url(r'^events/import/$', view='event_import', name='event_import'),
    url(r'^events/export/$', view='event_export', name='event_export_all'),
    url(r'^events/(?P<id>\d+)/$', view='event_detail', name='event_detail'),
    url(r'^events/(?P<id>\d+)/export/$', view='event_export', name='event_export'),
    url(r'^events/(?P<id>\d+)/edit/$', view='event_edit', name='event_edit'),
    url(r'^events/(?P<id>\d+)/delete/$', view='event_delete', name='event_delete'),
    url(r'^events/(?P<id>\d+)/move/(?P<days>[\d\-]+)/(?P<minutes>[\d\-]+)/$', view='event_move', name='event_move'),
    url(r'^events/(?P<id>\d+)/resize/(?P<days>[\d\-]+)/(?P<minutes>[\d\-]+)/$', view='event_resize', name='event_resize'),
    url(r'^events/(?P<id>\d+)/timeline/$', 'event_detail', {'template_name': 'calendar/event_timeline.html'}, 'event_timeline'),
)
