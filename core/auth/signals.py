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

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from prometeo.core.menus.signals import manage_bookmarks
from prometeo.core.widgets.signals import manage_dashboard

from cache import LoggedInUserCache
from models import *

## HANDLERS ##

def user_post_save(sender, instance, signal, *args, **kwargs):
    """Creates a profile for the given user.
    """
    profile, is_new = UserProfile.objects.get_or_create(user=instance)
    if is_new:
        can_view_this_user, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_user", "auth", "user", instance.pk)
        can_change_this_user, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_user", "auth", "user", instance.pk)
        can_delete_this_user, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_user", "auth", "user", instance.pk)

        can_view_this_user.users.add(instance)
        can_change_this_user.users.add(instance)
        can_delete_this_user.users.add(instance)

def update_author_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the author of the given object.
    """
    author = LoggedInUserCache().current_user
    content_type = ContentType.objects.get_for_model(sender)
    app_label = content_type.app_label
    model_name = content_type.model

    if author:
        can_view_this_object, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_%s" % model_name, app_label, model_name, instance.pk)
        can_change_this_object, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_%s" % model_name, app_label, model_name, instance.pk)
        can_delete_this_object, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_%s" % model_name, app_label, model_name, instance.pk)

        can_view_this_object.users.add(author)
        can_change_this_object.users.add(author)
        can_delete_this_object.users.add(author)

## CONNECTIONS ##

models.signals.post_save.connect(user_post_save, User)

manage_bookmarks(UserProfile)
manage_dashboard(UserProfile)
