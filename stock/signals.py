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

from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_save, post_delete

from prometeo.core.auth.models import ObjectPermission
from prometeo.core.auth.signals import *
from prometeo.core.widgets.signals import *
from prometeo.core.notifications.signals import *

from models import *

## HANDLERS ##

def update_manager_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the manager of the given warehouse.
    """
    can_view_this_warehouse, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_warehouse", "stock", "warehouse", instance.pk)
    can_change_this_warehouse, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_warehouse", "stock", "warehouse", instance.pk)
    can_delete_this_warehouse, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_warehouse", "stock", "warehouse", instance.pk)

    if instance.manager:
        can_view_this_warehouse.users.add(instance.manager)
        can_change_this_warehouse.users.add(instance.manager)
        can_delete_this_warehouse.users.add(instance.manager)

## CONNECTIONS ##

post_save.connect(update_author_permissions, Warehouse, dispatch_uid="update_warehouse_permissions")
post_save.connect(update_manager_permissions, Warehouse, dispatch_uid="update_warehouse_permissions")
post_save.connect(update_author_permissions, Movement, dispatch_uid="update_movement_permissions")

post_save.connect(notify_object_created, Warehouse, dispatch_uid="warehouse_created")
post_delete.connect(notify_object_deleted, Warehouse, dispatch_uid="warehouse_deleted")

post_save.connect(notify_object_created, Movement, dispatch_uid="movement_created")
post_delete.connect(notify_object_deleted, Movement, dispatch_uid="movement_deleted")

manage_stream(Warehouse)

manage_dashboard(Warehouse)
