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

from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

from ..models import *

def install(sender, created_models, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    accounting_menu, is_new = Menu.objects.get_or_create(
        slug="accounting_menu",
        description=_("Main menu for accounting management")
    )

    salesinvoice_menu, is_new = Menu.objects.get_or_create(
        slug="salesinvoice_menu",
        description=_("Main menu for sales invoice model")
    )
    
    # Links.
    accounting_link, is_new = Link.objects.get_or_create(
        title=_("Accounting"),
        slug="accounting",
        description=_("Accounting management"),
        url=reverse("bankaccount_list"),
        submenu=accounting_menu,
        menu=main_menu
    )

    bankaccounts_link, is_new = Link.objects.get_or_create(
        title=_("Bank accounts"),
        slug="bank-account-list",
        description=_("Bank accounts management"),
        url=reverse("bankaccount_list"),
        menu=accounting_menu
    )

    salesinvoices_link, is_new = Link.objects.get_or_create(
        title=_("Sales invoices"),
        slug="sales-invoice-list",
        description=_("Sales invoices management"),
        url=reverse("salesinvoice_list"),
        menu=accounting_menu
    )

    salesinvoice_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="sales-invoice-details",
        url="{% url salesinvoice_detail object.object_id %}",
        menu=salesinvoice_menu
    )

    salesinvoice_hard_copies_link, is_new = Link.objects.get_or_create(
        title=_("Hard copies"),
        slug="sales-invoice-hard-copies",
        url="{% url salesinvoice_hardcopies object.object_id %}",
        menu=salesinvoice_menu
    )

    salesinvoice_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="sales-invoice-timeline",
        url="{% url salesinvoice_timeline object.object_id %}",
        menu=salesinvoice_menu
    )
    
    # Signatures.
    bankaccount_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Bank account created"),
        slug="bank-account-created"
    )

    bankaccount_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Bank account deleted"),
        slug="bank-account-deleted"
    )

    salesinvoice_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Sales invoice created"),
        slug="salesinvoice-created"
    )

    salesinvoice_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Sales invoice changed"),
        slug="salesinvoice-changed"
    )

    salesinvoice_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Sales invoice deleted"),
        slug="salesinvoice-deleted"
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)
