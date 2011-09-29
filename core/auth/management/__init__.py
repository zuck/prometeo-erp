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

from prometeo.core.widgets.models import *
from prometeo.core.menus.models import *

def fixtures(sender, **kwargs):
    """Installs fixtures for this application.
    """
    main_menu = Menu.objects.get(slug="main")
    sidebar_region = Region.objects.get(slug="sidebar")
    
    # Menus.
    user_area_not_logged_menu = Menu.objects.create(
        slug="user_area_not_logged",
        description=_("User area for anonymous users")
    )
    
    user_area_logged_menu = Menu.objects.create(
        slug="user_area_logged",
        description=_("User area for logged users")
    )

    user_profile_menu = Menu.objects.create(
        slug="user_profile_menu",
        description=_("Main menu for user profiles")
    )
    
    # Links.
    dashboard_link = Link.objects.create(
        title=_("Dashboard"),
        slug="dashboard",
        description=_("Personal dashboard"),
        url="/",
        menu=main_menu
    )
    
    users_link = Link.objects.create(
        title=_("Users"),
        slug="users",
        description=_("Users management"),
        url=reverse("user_list"),
        menu=main_menu
    )
    
    login_link = Link.objects.create(
        title=_("Login"),
        slug="login",
        description=_("Login"),
        url=reverse("user_login"),
        only_authenticated=False,
        menu=user_area_not_logged_menu
    )
    
    administration_link = Link.objects.create(
        title=_("Administration"),
        slug="administration",
        description=_("Administration panel"),
        url="/admin",
        only_staff=True,
        menu=user_area_logged_menu
    )
    
    logout_link = Link.objects.create(
        title=_("Logout"),
        slug="logout",
        description=_("Logout"),
        url=reverse("user_logout"),
        menu=user_area_logged_menu
    )
    
    user_profile_details_link = Link.objects.create(
        title=_("Details"),
        slug="user_profile_details",
        url="{{ object.get_absolute_url }}",
        menu=user_profile_menu
    )
    
    user_profile_bookmarks_link = Link.objects.create(
        title=_("Bookmarks"),
        slug="user_profile_bookmarks",
        url="{% url bookmark_list object.username %}",
        menu=user_profile_menu
    )
    
    user_profile_notifications_link = Link.objects.create(
        title=_("Notifications"),
        slug="user_profile_notifications",
        url="{% url notification_list object.username %}",
        menu=user_profile_menu
    )

    # Widgets.
    profile_widget = Widget.objects.create(
        title=_("User Profile"),
        slug="user-profile",
        description=_("The user's profile"),
        source="prometeo.core.widgets.base.dummy",
        template="auth/widgets/user_profile.html",
        show_title=False,
        region=sidebar_region
    )
    
    post_syncdb.disconnect(fixtures)

post_syncdb.connect(fixtures)
