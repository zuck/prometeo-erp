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

from prometeo.core.utils import check_dependency
from prometeo.core.widgets.models import *
from prometeo.core.menus.models import *

check_dependency('prometeo.core.widgets')

def install(sender, **kwargs):
    sidebar_region, is_new = Region.objects.get_or_create(slug="sidebar")
    
    # Menus.
    main_menu, is_new = Menu.objects.get_or_create(
        slug="main",
        description=_("Main menu")
    )
    
    # Widgets.
    menu_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Menu"),
        slug="menu-widget-template",
        description=_("It renders a menu."),
        source="prometeo.core.widgets.base.dummy",
        template_name="menus/widgets/menu.html",
        context="{\"name\": \"\"}",
        public=False
    )

    main_menu_widget, is_new = Widget.objects.get_or_create(
        title=_("Main menu"),
        slug="main-menu",
        template=menu_widget_template,
        context="{\"name\": \"main\"}",
        show_title=False,
        sort_order=1,
        region=sidebar_region
    )

post_syncdb.connect(install, dispatch_uid="install_menus")
