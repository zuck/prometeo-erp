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

from datetime import date

def latest_events(context):
    """The list of latest events.
    """
    try:
        count = context['count']
    except KeyError:
        count = 5
    request = context['request']
    context['object_list'] = request.user.get_profile().calendar.event_set.all()[:count]
    return context

def today_events(context):
    """The list of events planned for the current day.
    """
    request = context['request']
    context['object_list'] = request.user.get_profile().calendar.event_set.filter(start__startswith=date.today())
    return context
