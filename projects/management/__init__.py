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

def fixtures(sender, **kwargs):
    """Installs fixtures for this application.
    """
    main_menu = Menu.objects.get(slug="main")

    # Menus.
    project_menu = Menu.objects.create(
        slug="project_menu",
        description=_("Main menu for projects")
    )

    milestone_menu = Menu.objects.create(
        slug="milestone_menu",
        description=_("Main menu for milestones")
    )

    ticket_menu = Menu.objects.create(
        slug="ticket_menu",
        description=_("Main menu for tickets")
    )
    
    # Links.
    projects_link = Link.objects.create(
        title=_("Projects"),
        slug="projects",
        description=_("Project management"),
        url=reverse("project_list"),
        menu=main_menu
    )

    project_dashboard_link = Link.objects.create(
        title=_("Dashboard"),
        slug="project_dashboard",
        url="{{ object.get_absolute_url }}",
        menu=project_menu
    )

    project_milestones_link = Link.objects.create(
        title=_("Milestones"),
        slug="project_milestones",
        url="{% url milestone_list object.slug %}",
        menu=project_menu
    )

    project_tickets_link = Link.objects.create(
        title=_("Tickets"),
        slug="project_tickets",
        url="{% url ticket_list object.slug %}",
        menu=project_menu
    )

    project_tickets_link = Link.objects.create(
        title=_("Timeline"),
        slug="project_timeline",
        url="{% url project_timeline object.slug %}",
        menu=project_menu
    )

    milestone_dashboard_link = Link.objects.create(
        title=_("Dashboard"),
        slug="milestone_dashboard",
        url="{{ object.get_absolute_url }}",
        menu=milestone_menu
    )

    milestone_tickets_link = Link.objects.create(
        title=_("Tickets"),
        slug="milestone_tickets",
        url="{% url milestone_tickets object.project.slug object.slug %}",
        menu=milestone_menu
    )

    ticket_details_link = Link.objects.create(
        title=_("Details"),
        slug="ticket_details",
        url="{{ object.get_absolute_url }}",
        menu=ticket_menu
    )
    
    post_syncdb.disconnect(fixtures)

post_syncdb.connect(fixtures)
