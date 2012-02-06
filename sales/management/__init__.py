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
from django.contrib.auth.models import Group

from prometeo.core.auth.models import MyPermission
from prometeo.core.utils import check_dependency
from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

from ..models import *

check_dependency('prometeo.core.widgets')
check_dependency('prometeo.core.menus')
check_dependency('prometeo.core.taxonomy')
check_dependency('prometeo.core.auth')
check_dependency('prometeo.documents')
check_dependency('prometeo.partners')

def install(sender, created_models, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    sales_menu, is_new = Menu.objects.get_or_create(
        slug="sales_menu",
        description=_("Main menu for sales management")
    )

    salesinvoice_menu, is_new = Menu.objects.get_or_create(
        slug="salesinvoice_menu",
        description=_("Main menu for sales invoice model")
    )
    
    # Links.
    sales_link, is_new = Link.objects.get_or_create(
        title=_("Sales"),
        slug="sales",
        description=_("Sales management"),
        url=reverse("bankaccount_list"),
        submenu=sales_menu,
        menu=main_menu
    )

    bankaccounts_link, is_new = Link.objects.get_or_create(
        title=_("Bank accounts"),
        slug="bank-account-list",
        description=_("Bank accounts management"),
        url=reverse("bankaccount_list"),
        menu=sales_menu
    )

    salesinvoices_link, is_new = Link.objects.get_or_create(
        title=_("Sales invoices"),
        slug="sales-invoice-list",
        description=_("Sales invoices management"),
        url=reverse("salesinvoice_list"),
        menu=sales_menu
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

    # Groups.
    sales_team_group, is_new = Group.objects.get_or_create(
        name=_('Sales Team')
    )

    sales_managers_group, is_new = Group.objects.get_or_create(
        name=_('Sales Managers')
    )

    # Permissions.
    can_view_bankaccount, is_new = MyPermission.objects.get_or_create_by_natural_key("view_bankaccount", "sales", "bankaccount")
    can_add_bankaccount, is_new = MyPermission.objects.get_or_create_by_natural_key("add_bankaccount", "sales", "bankaccount")
    can_change_bankaccount, is_new = MyPermission.objects.get_or_create_by_natural_key("change_bankaccount", "sales", "bankaccount")
    can_delete_bankaccount, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_bankaccount", "sales", "bankaccount")
    can_view_salesinvoice, is_new = MyPermission.objects.get_or_create_by_natural_key("view_salesinvoice", "sales", "salesinvoice")
    can_add_salesinvoice, is_new = MyPermission.objects.get_or_create_by_natural_key("add_salesinvoice", "sales", "salesinvoice")
    can_change_salesinvoice, is_new = MyPermission.objects.get_or_create_by_natural_key("change_salesinvoice", "sales", "salesinvoice")
    can_delete_salesinvoice, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_salesinvoice", "sales", "salesinvoice")

    sales_link.only_with_perms.add(can_view_bankaccount)
    bankaccounts_link.only_with_perms.add(can_view_bankaccount)
    salesinvoices_link.only_with_perms.add(can_view_salesinvoice)

    sales_team_group.permissions.add(can_view_bankaccount, can_add_bankaccount, can_view_salesinvoice, can_add_salesinvoice)
    sales_managers_group.permissions.add(can_view_bankaccount, can_add_bankaccount, can_change_bankaccount, can_delete_bankaccount, can_view_salesinvoice, can_add_salesinvoice, can_change_salesinvoice, can_delete_salesinvoice)

post_syncdb.connect(install, dispatch_uid="install_sales")
