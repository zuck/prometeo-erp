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

check_dependency('prometeo.core.widgets')

def install(sender, **kwargs):    
    # Widgets.
    categories_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Categories"),
        slug="categories-widget-template",
        description=_("It renders the category tree."),
        source="prometeo.core.taxonomy.widgets.categories",
        template_name="taxonomy/widgets/categories.html",
    )

    tag_cloud_widget_template, is_new = WidgetTemplate.objects.get_or_create(
        title=_("Tags cloud"),
        slug="tag-cloud-widget-template",
        description=_("It renders the tags cloud."),
        source="prometeo.core.taxonomy.widgets.tag_cloud",
        template_name="taxonomy/widgets/tag_cloud.html",
    )

post_syncdb.connect(install, dispatch_uid="install_taxonomy")
