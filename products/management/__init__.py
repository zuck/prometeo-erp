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
    product_menu, is_new = Menu.objects.get_or_create(
        slug="product_menu",
        description=_("Main menu for product model")
    )
    
    # Links.
    products_link, is_new = Link.objects.get_or_create(
        title=_("Products"),
        slug="products",
        description=_("Products management"),
        url=reverse("product_list"),
        menu=main_menu
    )

    product_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="product-details",
        url="{% url product_detail object.pk %}",
        menu=product_menu
    )

    product_supplies_link, is_new = Link.objects.get_or_create(
        title=_("Supplies"),
        slug="product-supplies",
        url="{% url product_supplies object.pk %}",
        menu=product_menu
    )

    product_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="product-timeline",
        url="{% url product_timeline object.pk %}",
        menu=product_menu
    )
    
    # Signatures.
    product_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Product created"),
        slug="product-created"
    )

    product_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Product deleted"),
        slug="product-deleted"
    )

    supply_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Product supply created"),
        slug="supply-created"
    )

    supply_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Product supply deleted"),
        slug="supply-deleted"
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)
