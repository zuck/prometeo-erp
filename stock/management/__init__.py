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

from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

from ..models import *

def install(sender, created_models, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    stock_menu, is_new = Menu.objects.get_or_create(
        slug="stock_menu",
        description=_("Main menu for stock management")
    )

    warehouse_menu, is_new = Menu.objects.get_or_create(
        slug="warehouse_menu",
        description=_("Main menu for warehouse model")
    )
    
    # Links.
    stock_link, is_new = Link.objects.get_or_create(
        title=_("Stock"),
        slug="stock",
        description=_("Stock management"),
        url=reverse("warehouse_list"),
        menu=main_menu
    )

    stock_warehouses_link, is_new = Link.objects.get_or_create(
        title=_("Warehouses"),
        slug="warehouse-list",
        description=_("Warehouses management"),
        url=reverse("warehouse_list"),
        menu=stock_menu
    )

    stock_movements_link, is_new = Link.objects.get_or_create(
        title=_("Movements"),
        slug="movement-list",
        description=_("Movements management"),
        url=reverse("movement_list"),
        menu=stock_menu
    )

    stock_delivery_notes_link, is_new = Link.objects.get_or_create(
        title=_("Delivery notes"),
        slug="delivery-note-list",
        description=_("Delivery notes management"),
        url=reverse("delivery_note_list"),
        menu=stock_menu
    )

    warehouse_details_link, is_new = Link.objects.get_or_create(
        title=_("Dashboard"),
        slug="warehouse-dashboard",
        url="{% url warehouse_detail object.pk %}",
        menu=warehouse_menu
    )

    warehouse_movements_link, is_new = Link.objects.get_or_create(
        title=_("Movements"),
        slug="warehouse-movements",
        url="{% url warehouse_movements object.pk %}",
        menu=warehouse_menu
    )

    warehouse_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="warehouse-timeline",
        url="{% url warehouse_timeline object.pk %}",
        menu=warehouse_menu
    )
    
    # Signatures.
    warehouse_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Warehouse created"),
        slug="warehouse-created"
    )

    warehouse_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Warehouse deleted"),
        slug="warehouse-deleted"
    )

    movement_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Movement created"),
        slug="movement-created"
    )

    movement_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Movement deleted"),
        slug="movement-deleted"
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)
