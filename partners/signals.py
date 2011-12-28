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

def update_assignee_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions of the assignee of the given partner.
    """
    can_view_this_partner, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_partner", "partners", "partner", instance.pk)
    can_change_this_partner, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_partner", "partners", "partner", instance.pk)
    can_delete_this_partner, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_partner", "partners", "partner", instance.pk)

    if instance.assignee:
        can_view_this_partner.users.add(instance.assignee)
        can_change_this_partner.users.add(instance.assignee)
        can_delete_this_partner.users.add(instance.assignee)

## CONNECTIONS ##

post_save.connect(update_author_permissions, Partner, dispatch_uid="update_partner_permissions")
post_save.connect(update_assignee_permissions, Partner, dispatch_uid="update_partner_permissions")
post_save.connect(update_author_permissions, Contact, dispatch_uid="update_contact_permissions")

post_save.connect(notify_object_created, Partner, dispatch_uid="partner_created")
post_change.connect(notify_object_changed, Partner, dispatch_uid="partner_changed")
post_delete.connect(notify_object_deleted, Partner, dispatch_uid="partner_deleted")

post_save.connect(notify_object_created, Contact, dispatch_uid="contact_created")
post_change.connect(notify_object_changed, Contact, dispatch_uid="contact_changed")
post_delete.connect(notify_object_deleted, Contact, dispatch_uid="contact_deleted")

post_save.connect(notify_object_created, Job, dispatch_uid="contact_added")
post_delete.connect(notify_object_deleted, Job, dispatch_uid="contact_removed")

manage_stream(Partner)

make_observable(Partner)
make_observable(Contact)

manage_dashboard(Partner)
