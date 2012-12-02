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
from django.db.models.signals import pre_save, post_save, post_delete

from prometeo.core.auth.models import ObjectPermission
from prometeo.core.auth.signals import *
from prometeo.core.widgets.signals import *
from prometeo.core.notifications.signals import *

from models import *

## HANDLERS ##

def update_manager_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the manager of the given object.
    """
    model_name = sender.__name__.lower()

    can_view_this_object, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_%s" % model_name, "projects", model_name, instance.pk)
    can_change_this_object, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_%s" % model_name, "projects", model_name, instance.pk)
    can_delete_this_object, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_%s" % model_name, "projects", model_name, instance.pk)

    if instance.manager:
        can_view_this_object.users.add(instance.manager)
        can_change_this_object.users.add(instance.manager)
        can_delete_this_object.users.add(instance.manager)

def update_assignee_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions of the assignee of the given ticket.
    """
    can_view_this_ticket, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_ticket", "projects", "ticket", instance.pk)
    can_change_this_ticket, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_ticket", "projects", "ticket", instance.pk)
    can_delete_this_ticket, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_ticket", "projects", "ticket", instance.pk)

    if instance.manager:
        can_view_this_ticket.users.add(instance.assignee)
        can_change_this_ticket.users.add(instance.assignee)
        can_delete_this_ticket.users.add(instance.assignee)

def link_project_stream(sender, instance, **kwargs):
    """Links the given stream to the parent project's one.
    """
    if instance.stream and instance.project:
        instance.stream.linked_streams.add(instance.project.stream)

def link_milestone_stream(sender, instance, **kwargs):
    """Links the given stream to the parent milestone's one.
    """
    if instance.stream and instance.milestone:
        instance.stream.linked_streams.add(instance.milestone.stream)

## CONNECTIONS ##

post_save.connect(update_author_permissions, Project, dispatch_uid="update_project_permissions")
post_save.connect(update_manager_permissions, Project, dispatch_uid="update_project_permissions")

post_save.connect(update_author_permissions, Milestone, dispatch_uid="update_milestone_permissions")
post_save.connect(update_manager_permissions, Milestone, dispatch_uid="update_milestone_permissions")

post_save.connect(update_author_permissions, Ticket, dispatch_uid="update_ticket_permissions")
post_save.connect(update_assignee_permissions, Ticket, dispatch_uid="update_ticket_permissions")

post_save.connect(notify_object_created, Project, dispatch_uid="project_created")
post_change.connect(notify_object_changed, Project, dispatch_uid="project_changed")
post_delete.connect(notify_object_deleted, Project, dispatch_uid="project_deleted")

pre_save.connect(link_project_stream, Milestone, dispatch_uid="link_project_stream")
post_save.connect(notify_object_created, Milestone, dispatch_uid="milestone_created")
post_change.connect(notify_object_changed, Milestone, dispatch_uid="milestone_changed")
post_delete.connect(notify_object_deleted, Milestone, dispatch_uid="milestone_deleted")

pre_save.connect(link_project_stream, Ticket, dispatch_uid="link_project_stream")
pre_save.connect(link_milestone_stream, Ticket, dispatch_uid="link_milestone_stream")
post_save.connect(notify_object_created, Ticket, dispatch_uid="ticket_created")
post_change.connect(notify_object_changed, Ticket, dispatch_uid="ticket_changed")
post_delete.connect(notify_object_deleted, Ticket, dispatch_uid="ticket_deleted")

make_observable(Project)
make_observable(Milestone)
make_observable(Ticket)

manage_dashboard(Project)
manage_dashboard(Milestone)
