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

from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_save, post_delete, m2m_changed

from prometeo.core.auth.models import *
from prometeo.core.auth.signals import *
from prometeo.core.notifications.signals import *

from models import *

## UTILS ##

def manage_calendar(cls):
    """Connects handlers for calendar management.
    """
    models.signals.post_save.connect(create_calendar, cls)
    models.signals.post_delete.connect(delete_calendar, cls)

## HANDLERS ##

def update_attendees_event_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the attendees of the given event.
    """
    can_view_this_event, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_event", "calendar", "event", instance.pk)
    can_change_this_event, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_event", "calendar", "event", instance.pk)

    for att in instance.attendees.all():
        can_view_this_event.users.add(att)
        can_change_this_event.users.add(att)

def create_calendar(sender, instance, *args, **kwargs):
    """Updates the calendar field of the object's stream.
    """
    if hasattr(instance, "calendar") and not instance.calendar:
        calendar, is_new = Calendar.objects.get_or_create(
            title="%s's calendar" % instance,
            slug="%s_%d_calendar" % (sender.__name__.lower(), instance.pk),
            description=_("Calendar for %s") % instance
        )
        if not is_new:
            for e in calendar.events.all():
                e.delete()
        instance.calendar = calendar
        instance.save()

def delete_calendar(sender, instance, *args, **kwargs):
    """Deletes the calendar of the given object.
    """
    calendar = instance.calendar
    if calendar:
        calendar.delete()
        instance.calendar = None

## CONNECTIONS ##

post_save.connect(update_author_permissions, Event, dispatch_uid="update_event_permissions")
m2m_changed.connect(update_attendees_event_permissions, Event.attendees.through, dispatch_uid="update_event_permissions")

post_save.connect(notify_object_created, Event, dispatch_uid="event_created")
post_change.connect(notify_object_changed, Event, dispatch_uid="event_changed")
post_delete.connect(notify_object_deleted, Event, dispatch_uid="event_deleted")

m2m_changed.connect(notify_m2m_changed, Event.attendees.through, dispatch_uid="attendees_changed")

manage_stream(Event)
make_observable(Event)

manage_calendar(UserProfile)
