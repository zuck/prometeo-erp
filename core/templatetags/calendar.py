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

from datetime import datetime, date, time, timedelta

from django import template
from django.utils.datastructures import SortedDict
from django.template.loader import render_to_string

register = template.Library()

def get_first_day_of_week(year, week):
    """Returns the first date of the given week.
    """
    d = date(year, 1, 1)
    return d + timedelta(days=-d.weekday(), weeks=week)

def get_last_day_of_month(year, month):
    """Returns the last date of the given month.
    """
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1

    return date(year, month, 1) - timedelta(1)

def get_events_for_day(year, month, day, event_list):
    """Returns a dictionary of events for the given day.
    
    Events are ordered by hour.
    """
    current_day = date(year, month, day)

    day_events = SortedDict([(time(hour, 0, 0), []) for hour in range(24)])

    for event in event_list:
        if event.start.date() == current_day:
            day_events[event.start.time().replace(minute=0, second=0, microsecond=0)].append(event)

    return day_events

def get_events_for_week(year, week, event_list):
    """Returns a dictionary of events for the given week.
    
    Events are ordered by day and hour.
    """
    first_week_day = get_first_day_of_week(year, week)
    week_events = SortedDict([(first_week_day + timedelta(i), {}) for i in range(7)])

    for wk_day in week_events.keys():
        week_events[wk_day] = get_events_for_day(wk_day.year, wk_day.month, wk_day.day, event_list)

    return week_events

def get_events_for_month(year, month, event_list):
    """Returns a dictionary of events for the given month.
    
    Events are ordered by week, day and hour.
    """
    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())

    month_events = SortedDict()

    day = first_day_of_calendar

    while day <= last_day_of_month:
        month_events[day] = get_events_for_week(day.year, day.isocalendar()[1], event_list)
        day += timedelta(7)

    return month_events

def get_events_for_year(year, event_list):
    """Returns a dictionary of events for the given year.
    
    Events are ordered by month, week, day and hour.
    """
    year_events = SortedDict([(date(int(year), i+1, 1), []) for i in range(12)])

    for month in year_events.keys():
        year_events[month] = get_events_for_month(year, month.month, event_list)

    return year_events

@register.simple_tag(takes_context=True)
def day_calendar(context, year, month, day, event_list, template_name="elements/day_calendar.html"):
    """Renders a day calendar.
    """
    context['hour_headers'] = [i for i in range(1, 24)]
    context['calendar'] = get_events_for_day(int(year), int(month), int(day), event_list)

    return render_to_string(template_name, context)

@register.simple_tag(takes_context=True)
def week_calendar(context, year, week, event_list, template_name="elements/week_calendar.html"):
    """Renders a week calendar.
    """
    context['hour_headers'] = [i for i in range(0, 24)]
    context['calendar'] = get_events_for_week(int(year), int(week), event_list)

    return render_to_string(template_name, context)

@register.simple_tag(takes_context=True)
def month_calendar(context, year, month, event_list, template_name="elements/month_calendar.html"):
    """Renders a month calendar.
    """
    context['month'] = month
    context['calendar'] = get_events_for_month(int(year), int(month), event_list)

    return render_to_string(template_name, context)

@register.simple_tag(takes_context=True)
def year_calendar(context, year, event_list, template_name="elements/year_calendar.html"):
    """Renders a year calendar.
    """
    context['calendar'] = get_events_for_year(int(year), event_list)

    return render_to_string(template_name, context)
