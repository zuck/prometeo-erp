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

import json
from datetime import datetime, timedelta

import icalendar

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.date_based import archive_day, archive_week, archive_month, archive_year
from django.views.generic.simple import redirect_to
from django.template.defaultfilters import slugify
from django.http import HttpResponse
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.core.utils import clean_referer

from models import *
from forms import *

def _get_event(request, *args, **kwargs):
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(Event, id=id)
    return None

def _current_day(year=None, month=None, day=None, week=None):
    """Tries to return the best matched day for the given data.
    """
    result = datetime.datetime.now()

    if year:
        result = result.replace(year=int(year))

    if week:
        jan1 = datetime.date(result.year, 1, 1)
        wd1 = jan1 + datetime.timedelta(days=-jan1.weekday(), weeks=int(week))
        result = result.replace(month=wd1.month)
        result = result.replace(day=wd1.day)

    if month:
        result = result.replace(month=int(month))

    if day:
        result = result.replace(day=int(day))

    return result

@permission_required('calendar.view_calendar') 
def event_list(request, year=None, month=None, day=None, page=0, paginate_by=10, **kwargs):
    """Displays the list of all calendar for the request user.
    """
    return filtered_list_detail(
        request,
        Event.objects.for_user(request.user),
        paginate_by=paginate_by,
        page=page,
        fields=['title', 'start', 'end', 'created'],
        extra_context={
            'current_day': _current_day(year, month, day),
        },
        **kwargs
    )

@permission_required('calendar.view_calendar') 
def event_day(request, year=None, month=None, day=None, **kwargs):
    """Displays the list of calendar for the given day.
    """
    current_day = _current_day(year, month, day)
    previous_day = current_day - datetime.timedelta(1)
    next_day = current_day + datetime.timedelta(1)

    return archive_day(
        request,
        year=year,
        month=month,
        day=day,
        queryset=Event.objects.for_user(request.user),
        date_field="start",
        month_format="%m",
        allow_empty=True,
        allow_future=True,
        template_name="calendar/event_day.html",
        extra_context={
            'previous_day': previous_day,
            'next_day': next_day,
            'current_day': current_day
        },
        **kwargs
    )

@permission_required('calendar.view_calendar') 
def event_week(request, year=None, week=None, **kwargs):
    """Displays the list of calendar for the given week.
    """
    current_day = _current_day(year, week=week)
    previous_week = current_day - datetime.timedelta(weeks=1)
    next_week = current_day + datetime.timedelta(weeks=1)

    return archive_week(
        request,
        year=year,
        week=week,
        queryset=Event.objects.for_user(request.user),
        date_field="start",
        allow_empty=True,
        allow_future=True,
        template_name="calendar/event_week.html",
        extra_context={
            'previous_week': previous_week,
            'next_week': next_week,
            'current_day': current_day
        },
        **kwargs
    )

@permission_required('calendar.view_calendar') 
def event_month(request, year=None, month=None, **kwargs):
    """Displays the list of calendar for the given month.
    """
    current_day = _current_day(year, month)
    previous_month = current_day - datetime.timedelta(days=30)
    next_month = current_day + datetime.timedelta(days=30)

    return archive_month(
        request,
        year=year,
        month=month,
        queryset=Event.objects.for_user(request.user),
        date_field="start",
        month_format="%m",
        allow_empty=True,
        allow_future=True,
        template_name="calendar/event_month.html",
        extra_context={
            'previous_year': previous_month,
            'next_year': next_month,
            'current_day':  current_day
        },
        **kwargs
    )

@permission_required('calendar.view_calendar') 
def event_year(request, year=None, **kwargs):
    """Displays the list of calendar for the given year.
    """
    current_day = _current_day(year)
    previous_year = current_day - datetime.timedelta(days=365)
    next_year = current_day + datetime.timedelta(days=365)

    return archive_year(
        request,
        year=year,
        queryset=Event.objects.for_user(request.user),
        date_field="start",
        allow_empty=True,
        allow_future=True,
        template_name="calendar/event_year.html",
        extra_context={
            'previous_year': previous_year,
            'next_year': next_year,
            'current_day': current_day
        },
        **kwargs
    )

@permission_required('calendar.view_event', _get_event)
def event_detail(request, id, **kwargs):
    """Displays an event.
    """
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=Event.objects.for_user(request.user),
        **kwargs
    )

@permission_required('calendar.add_event') 
def event_add(request, year=None, month=None, day=None, **kwargs):
    """Adds a new event.
    """
    start = datetime.datetime.now()
    if year and month and day:
        start = datetime.datetime.combine(datetime.date(int(year), int(month), int(day)), start.time())

    event = Event(author=request.user, start=start)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            event.calendars.add(request.user.get_profile().calendar)
            messages.success(request, _("The event was created successfully."))
            return redirect_to(request, url=event.get_absolute_url())
    else:
        form = EventForm(instance=event)

    return render_to_response('calendar/event_edit.html', RequestContext(request, {'form': form, 'object': event}))

@permission_required('calendar.change_event', _get_event) 
def event_edit(request, id, **kwargs):
    """Edits an event.
    """
    return create_update.update_object(
        request,
        form_class=EventForm,
        object_id=id,
        template_name='calendar/event_edit.html',
        **kwargs
    )

@permission_required('calendar.delete_event', _get_event) 
def event_delete(request, id, **kwargs):
    """Deletes an event.
    """
    return create_update.delete_object(
            request,
            model=Event,
            object_id=id,
            post_delete_redirect='/calendar/',
            template_name='calendar/event_delete.html',
            **kwargs
        )

@permission_required('calendar.add_event') 
def event_import(request, **kwargs):
    """Imports one or more calendar from an .ics file.
    """
    if request.method == 'POST':
        form = ImportEventsForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            stream = ""
            for chunk in f.chunks():
                stream += chunk
            try:
                cals = icalendar.Calendar.from_string(stream, True)
                for cal in cals:
                    for evt in cal.walk('VEVENT'):
                        event, new = Event.objects.get_or_create(
                            title=evt.decoded('summary', _("Empty event")),
                            start=evt.decoded('dtstart', datetime.datetime.now()),
                            end=evt.decoded('dtend', datetime.datetime.now()),
                            location=evt.decoded('location', ""),
                            description=evt.decoded('description', ""),
                            status=evt.decoded('status', settings.EVENT_DEFAULT_STATUS),
                            author=request.user
                        )
                        messages.success(request, _("Event \"%s\" has been imported.") % event.title)
                return redirect_to(request, url=reverse("event_list"))
            except ValueError:
                messages.error(request, _("Sorry, an error has occurred during importing of calendar."))
    else:
        form = ImportEventsForm()

    return render_to_response('calendar/event_import.html', RequestContext(request, {'form': form}))

@permission_required('calendar.view_calendar')
def event_export(request, id=None, **kwargs):
    """Exports one or more calendar as an .ics file.
    """
    filename = "%s-calendar.ics" % (request.user)

    queryset = Event.objects.for_user(request.user)

    if id:
        calendar = [get_object_or_404(queryset, id=id)]
        filename = u'%s.ics' % slugify(calendar[0].title)
    else:
        calendar = list(queryset)

    cal = icalendar.Calendar()
    cal.add('prodid', '-//Prometeo ERP//')
    cal.add('method', 'PUBLISH')  # IE/Outlook needs this.
    cal.add('version', '2.0')

    for event in calendar:
        evt = icalendar.Event()

        evt['uid'] = event.pk
        evt.add('summary', event.title)
        evt.add('status', event.status)
        evt.add('created', event.created)
        evt.add('dtstamp', event.start)
        evt.add('dtstart', event.start)
        if event.end:
            evt.add('dtend', event.end)
        if event.location:
            evt.add('location', event.location)
        if event.description:
            evt.add('description', event.description)

        cal.add_component(evt)

    response = HttpResponse(cal.as_string(), mimetype='text/calendar')
    response['Filename'] = filename # IE needs this.
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@permission_required('calendar.change_event', _get_event) 
def event_move(request, id, days, minutes, **kwargs):
    """Move an event forward or backward.
    """
    evt = Event.objects.get(pk=id)
    
    evt.start = evt.start + timedelta(int(days)) + timedelta(0, 0, 0, 0, int(minutes))
    evt.end = evt.end + timedelta(int(days)) + timedelta(0, 0, 0, 0, int(minutes))
    evt.save()

    if request.is_ajax():
        resp = {"status": "OK"}
        return HttpResponse(simplejson.dumps(resp))
    else:
        return redirect_to(request, permanent=False, url=clean_referer(request, reverse("event_list")))

@permission_required('calendar.change_event', _get_event) 
def event_resize(request, id, days, minutes, **kwargs):
    """Resize an event duration.
    """
    evt = Event.objects.get(pk=id)
    
    evt.end = evt.end + timedelta(int(days)) + timedelta(0, 0, 0, 0, int(minutes))
    evt.save()

    if request.is_ajax():
        resp = {"status": "OK"}
        return HttpResponse(simplejson.dumps(resp))
    else:
        return redirect_to(request, permanent=False, url=clean_referer(request, reverse("event_list")))
