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

from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.menus.models import *

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    todo_menu, is_new = Menu.objects.get_or_create(
        slug="todo_menu",
        description=_("Main menu for tasks")
    )
    
    # Links.
    tasks_link, is_new = Link.objects.get_or_create(
        title=_("Tasks"),
        slug="tasks",
        description=_("List of tasks"),
        url="{% url task_list %}",
        submenu=todo_menu,
        menu=main_menu
    )

    planned_tasks_link, is_new = Link.objects.get_or_create(
        title=_("Planned"),
        slug="planned_tasks",
        url="{% url task_list %}",
        menu=todo_menu
    )

    unplanned_tasks_link, is_new = Link.objects.get_or_create(
        title=_("Unplanned"),
        slug="unplanned_tasks",
        url="{% url unplanned_task_list %}",
        menu=todo_menu
    )

    timesheets_link, is_new = Link.objects.get_or_create(
        title=_("Timesheets"),
        slug="timesheets",
        url="{% url timesheet_list %}",
        menu=todo_menu
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)
