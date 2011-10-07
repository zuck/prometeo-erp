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

from django.core.urlresolvers import reverse
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

def fixtures(sender, **kwargs):
    """Installs fixtures for this application.
    """
    main_menu = Menu.objects.get(slug="main")

    # Menus.
    events_menu = Menu.objects.create(
        slug="events_menu",
        description=_("Main menu for events")
    )

    event_menu = Menu.objects.create(
        slug="event_menu",
        description=_("Main menu for event")
    )
    
    # Links.
    events_link = Link.objects.create(
        title=_("Events"),
        slug="events",
        description=_("Event planning"),
        url=reverse("event_list"),
        menu=main_menu
    )

    events_agenda_link = Link.objects.create(
        title=_("Agenda"),
        slug="events_agenda",
        url="{% url event_list %}",
        menu=events_menu
    )

    events_day_link = Link.objects.create(
        title=_("Day"),
        slug="events_day",
        url="{% url event_day current_day.year current_day.month current_day.day %}",
        menu=events_menu
    )

    events_week_link = Link.objects.create(
        title=_("Week"),
        slug="events_week",
        url="{% url event_week current_day.year current_day|date:'W' %}",
        menu=events_menu
    )

    events_month_link = Link.objects.create(
        title=_("Month"),
        slug="events_month",
        url="{% url event_month current_day.year current_day.month %}",
        menu=events_menu
    )

    events_year_link = Link.objects.create(
        title=_("Year"),
        slug="events_year",
        url="{% url event_year current_day.year %}",
        menu=events_menu
    )

    event_dashboard_link = Link.objects.create(
        title=_("Dashboard"),
        slug="event_dashboard",
        url="{{ object.get_absolute_url }}",
        menu=event_menu
    )

    event_timeline_link = Link.objects.create(
        title=_("Timeline"),
        slug="event_timeline",
        url="{% url event_timeline object.pk %}",
        menu=event_menu
    )

    # Signatures.
    event_created_signature = Signature.objects.create(
        title=_("Event created"),
        slug="event-created"
    )

    event_changed_signature = Signature.objects.create(
        title=_("Event changed"),
        slug="event-changed"
    )

    event_deleted_signature = Signature.objects.create(
        title=_("Event deleted"),
        slug="event-deleted"
    )
    
    post_syncdb.disconnect(fixtures)

post_syncdb.connect(fixtures)
