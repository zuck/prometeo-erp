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

from django.db import models
from django.utils.translation import ugettext_noop as _

from models import *

## HANDLERS ##

def create_dashboard(sender, instance, *args, **kwargs):
    """Creates a new dashboard for the given object.
    """
    if not instance.dashboard:
        instance.dashboard = Region.objects.create(slug="%s_dashboard" % sender.__name__.lower(), description=_("Dashboard"))

def update_dashboard(sender, instance, *args, **kwargs):
    """Updates the slug field of the object's dashboard.
    """
    dashboard = instance.dashboard
    if dashboard:
        dashboard.slug = "%s_%d_dashboard" % (sender.__name__.lower(), instance.pk)
        dashboard.save()

def delete_dashboard(sender, instance, *args, **kwargs):
    """Deletes the dashboard of the given object.
    """
    dashboard = instance.dashboard
    if dashboard:
        dashboard.delete()

## CONNECTORS ##

def manage_dashboard(cls):
    models.signals.pre_save.connect(create_dashboard, cls)
    models.signals.post_save.connect(update_dashboard, cls)
    models.signals.post_delete.connect(delete_dashboard, cls)
