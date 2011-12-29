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

from prometeo.core.widgets.models import *

def install(sender, **kwargs):
    # Regions.
    footer_region, is_new = Region.objects.get_or_create(
        slug="footer",
        description=_("Footer")
    )
    
    sidebar_region, is_new = Region.objects.get_or_create(
        slug="sidebar",
        description=_("Sidebar")
    )
    
    # Widgets.
    text_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Simple text"),
        slug="text-widget-template",
        description=_("It renders a text message."),
        source="prometeo.core.widgets.base.dummy",
        template_name="widgets/widget.html",
        context="{\"text\": \"\"}",
    )

    powered_by_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Powered by"),
        slug="powered-by-widget-template",
        description=_("Info about Prometeo."),
        source="prometeo.core.widgets.base.dummy",
        template_name="widgets/powered-by.html",
        context="{\"text\": \"Prometeo\", \"url\": \"http://code.google.com/p/prometeo-erp/\"}",
        public=False,
    )

    powered_by_widget, is_new = Widget.objects.get_or_create(
        title=_("Powered by"),
        slug="powered-by",
        template=powered_by_widget_template,
        show_title=False,
        region=footer_region
    )

post_syncdb.connect(install, dispatch_uid="install_widgets")
