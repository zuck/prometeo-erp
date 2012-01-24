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

from django.core.urlresolvers import reverse
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _
from django.contrib.auth.models import Group

from prometeo.core.auth.models import MyPermission
from prometeo.core.utils import check_dependency
from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature
from prometeo.core.widgets.models import *

check_dependency('prometeo.core.widgets')
check_dependency('prometeo.core.menus')
check_dependency('prometeo.core.taxonomy')
check_dependency('prometeo.core.auth')
check_dependency('prometeo.core.notifications')

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")
    users_group, is_new = Group.objects.get_or_create(name=_('Users'))

    # Menus.
    calendar_menu, is_new = Menu.objects.get_or_create(
        slug="calendar-menu",
        description=_("Main menu for calendar")
    )

    event_menu, is_new = Menu.objects.get_or_create(
        slug="event-menu",
        description=_("Main menu for event")
    )
    
    # Links.
    calendar_link, is_new = Link.objects.get_or_create(
        title=_("Calendar"),
        slug="calendar",
        description=_("Events planning"),
        url="{% url event_list %}",
        menu=main_menu,
        submenu=calendar_menu
    )

    events_agenda_link, is_new = Link.objects.get_or_create(
        title=_("Agenda"),
        slug="events-agenda",
        url="{% url event_list %}",
        menu=calendar_menu
    )

    events_day_link, is_new = Link.objects.get_or_create(
        title=_("Day"),
        slug="events-day",
        url="{% url event_day current_day.year|default:today.year current_day.month|default:today.month current_day.day|default:today.day %}",
        menu=calendar_menu
    )

    events_week_link, is_new = Link.objects.get_or_create(
        title=_("Week"),
        slug="events-week",
        url="{% url event_week current_day.year|default:today.year current_day|default:today|date:'W' %}",
        menu=calendar_menu
    )

    events_month_link, is_new = Link.objects.get_or_create(
        title=_("Month"),
        slug="events-month",
        url="{% url event_month current_day.year|default:today.year current_day.month|default:today.month %}",
        menu=calendar_menu
    )

    events_year_link, is_new = Link.objects.get_or_create(
        title=_("Year"),
        slug="events-year",
        url="{% url event_year current_day.year|default:today.year %}",
        menu=calendar_menu
    )

    event_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="event-details",
        url="{{ object.get_absolute_url }}",
        menu=event_menu
    )

    event_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="event-timeline",
        url="{% url event_timeline object.pk %}",
        menu=event_menu
    )

    # Signatures.
    event_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Event created"),
        slug="event-created"
    )

    event_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Event changed"),
        slug="event-changed"
    )

    event_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Event deleted"),
        slug="event-deleted"
    )

    # Permissions.
    can_view_calendar, is_new = MyPermission.objects.get_or_create_by_natural_key("view_calendar", "calendar", "calendar")
    can_add_event, is_new = MyPermission.objects.get_or_create_by_natural_key("add_event", "calendar", "event")

    users_group.permissions.add(can_view_calendar, can_add_event)

    calendar_link.only_with_perms.add(can_view_calendar)

    # Widgets.
    latest_events_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Latest events"),
        slug="events-widget-template",
        description=_("It renders the list of the latest events."),
        source="prometeo.core.calendar.widgets.latest_events",
        template_name="calendar/widgets/latest_events.html",
    )

    today_events_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Today events"),
        slug="today-events-widget-template",
        description=_("It renders the list of the today events."),
        source="prometeo.core.calendar.widgets.today_events",
        template_name="calendar/widgets/latest_events.html",
    )

post_syncdb.connect(install, dispatch_uid="install_calendar")
