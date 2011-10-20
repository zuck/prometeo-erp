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

from django.db.models.signals import post_save

from prometeo.core.auth.models import ObjectPermission

from models import *

## HANDLERS ##

def update_owner_task_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the owner of the given task.
    """
    # Change task.
    can_change_this_task, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_task", "todo", "task", instance.pk)
    can_change_this_task.users.add(instance.user)
    # Delete task.
    can_delete_this_task, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_task", "todo", "task", instance.pk)
    can_delete_this_task.users.add(instance.user)

def update_owner_timesheet_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the owner of the given timesheet.
    """
    # Change timesheet.
    can_change_this_timesheet, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_timesheet", "todo", "timesheet", instance.pk)
    can_change_this_timesheet.users.add(instance.user)
    # Delete timesheet.
    can_delete_this_timesheet, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_timesheet", "todo", "timesheet", instance.pk)
    can_delete_this_timesheet.users.add(instance.user)

## CONNECTIONS ##

post_save.connect(update_owner_task_permissions, Task, dispatch_uid="update_task_permissions")
post_save.connect(update_owner_timesheet_permissions, Timesheet, dispatch_uid="update_timesheet_permissions")
