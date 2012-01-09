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

from prometeo.core.auth.models import MyPermission
from prometeo.core.menus.models import *
from prometeo.core.utils import check_dependency

check_dependency('prometeo.core.menus')
check_dependency('prometeo.core.auth')

def install(sender, **kwargs):
    user_profile_menu, is_new = Menu.objects.get_or_create(slug="user_profile_menu", description=_("Main menu for user profiles"))

    # Links.
    user_profile_notifications_link, is_new = Link.objects.get_or_create(
        title=_("Notifications"),
        slug="user_profile_notifications",
        url="{% url notification_list object.username %}",
        menu=user_profile_menu
    )

    # Permissions.
    can_view_notification, is_new = MyPermission.objects.get_or_create_by_natural_key("view_notification", "notifications", "notification")

    user_profile_notifications_link.only_with_perms.add(can_view_notification)

post_syncdb.connect(install, dispatch_uid="install_notifications")
