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
from django.contrib.auth.models import Group

from prometeo.core.auth.models import MyPermission
from prometeo.core.utils import check_dependency
from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

check_dependency('prometeo.core.widgets')
check_dependency('prometeo.core.menus')
check_dependency('prometeo.core.taxonomy')
check_dependency('prometeo.core.auth')
check_dependency('prometeo.partners')
check_dependency('prometeo.documents')

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    hr_menu, is_new = Menu.objects.get_or_create(
        slug="hr_menu",
        description=_("Main menu for human resources")
    )

    employee_menu, is_new = Menu.objects.get_or_create(
        slug="employee_menu",
        description=_("Main menu for employee")
    )

    timesheet_menu, is_new = Menu.objects.get_or_create(
        slug="timesheet_menu",
        description=_("Main menu for timesheet")
    )

    expensevoucher_menu, is_new = Menu.objects.get_or_create(
        slug="expensevoucher_menu",
        description=_("Main menu for expense voucher")
    )

    leaverequest_menu, is_new = Menu.objects.get_or_create(
        slug="leaverequest_menu",
        description=_("Main menu for leave request")
    )
    
    # Links.
    hr_link, is_new = Link.objects.get_or_create(
        title=_("Human resources"),
        slug="hr",
        description=_("Human resources management"),
        url="{% if perms.hr.view_employee %}{% url employee_list %}{% else %}{% url timesheet_list %}{% endif %}",
        submenu=hr_menu,
        menu=main_menu
    )

    employees_link, is_new = Link.objects.get_or_create(
        title=_("Employees"),
        slug="employees",
        url="{% url employee_list %}",
        menu=hr_menu
    )

    timesheets_link, is_new = Link.objects.get_or_create(
        title=_("Timesheets"),
        slug="timesheets",
        url="{% url timesheet_list %}",
        menu=hr_menu
    )

    expensevouchers_link, is_new = Link.objects.get_or_create(
        title=_("Expense vouchers"),
        slug="expensevouchers",
        url="{% url expensevoucher_list %}",
        menu=hr_menu
    )

    leaverequests_link, is_new = Link.objects.get_or_create(
        title=_("Leave requests"),
        slug="leaverequests",
        url="{% url leaverequest_list %}",
        menu=hr_menu
    )

    employee_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="employee-details",
        url="{% url employee_detail object.pk %}",
        menu=employee_menu
    )

    timesheet_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="timesheet-details",
        url="{% url timesheet_detail object.object_id %}",
        menu=timesheet_menu
    )

    timesheet_hard_copies_link, is_new = Link.objects.get_or_create(
        title=_("Hard copies"),
        slug="timesheet-hard-copies",
        url="{% url timesheet_hardcopies object.object_id %}",
        menu=timesheet_menu
    )

    timesheet_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="timesheet-timeline",
        url="{% url timesheet_timeline object.object_id %}",
        menu=timesheet_menu
    )

    expensevoucher_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="expensevoucher-details",
        url="{% url expensevoucher_detail object.object_id %}",
        menu=expensevoucher_menu
    )

    expensevoucher_hard_copies_link, is_new = Link.objects.get_or_create(
        title=_("Hard copies"),
        slug="expensevoucher-hard-copies",
        url="{% url expensevoucher_hardcopies object.object_id %}",
        menu=expensevoucher_menu
    )

    expensevoucher_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="expensevoucher-timeline",
        url="{% url expensevoucher_timeline object.object_id %}",
        menu=expensevoucher_menu
    )

    leaverequest_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="leaverequest-details",
        url="{% url leaverequest_detail object.object_id %}",
        menu=leaverequest_menu
    )

    leaverequest_hard_copies_link, is_new = Link.objects.get_or_create(
        title=_("Hard copies"),
        slug="leaverequest-hard-copies",
        url="{% url leaverequest_hardcopies object.object_id %}",
        menu=leaverequest_menu
    )

    leaverequest_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="leaverequest-timeline",
        url="{% url leaverequest_timeline object.object_id %}",
        menu=leaverequest_menu
    )

    # Signatures.
    employee_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Employee created"),
        slug="employee-created"
    )

    employee_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Employee changed"),
        slug="employee-changed"
    )

    employee_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Employee deleted"),
        slug="employee-deleted"
    )

    timesheet_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Timesheet created"),
        slug="timesheet-created"
    )

    timesheet_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Timesheet changed"),
        slug="timesheet-changed"
    )

    timesheet_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Timesheet deleted"),
        slug="timesheet-deleted"
    )

    expensevoucher_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Expense voucher created"),
        slug="expensevoucher-created"
    )

    expensevoucher_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Expense voucher changed"),
        slug="expensevoucher-changed"
    )

    expensevoucher_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Expense voucher deleted"),
        slug="expensevoucher-deleted"
    )

    leaverequest_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Leave request created"),
        slug="leaverequest-created"
    )

    leaverequest_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Leave request changed"),
        slug="leaverequest-changed"
    )

    leaverequest_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Leave request deleted"),
        slug="leaverequest-deleted"
    )

    # Groups.
    employees_group, is_new = Group.objects.get_or_create(
        name=_('Employees')
    )

    hr_managers_group, is_new = Group.objects.get_or_create(
        name=_('HR Managers')
    )

    # Permissions.
    can_view_employee, is_new = MyPermission.objects.get_or_create_by_natural_key("view_employee", "hr", "employee")
    can_add_employee, is_new = MyPermission.objects.get_or_create_by_natural_key("add_employee", "hr", "employee")
    can_change_employee, is_new = MyPermission.objects.get_or_create_by_natural_key("change_employee", "hr", "employee")
    can_delete_employee, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_employee", "hr", "employee")
    can_view_timesheet, is_new = MyPermission.objects.get_or_create_by_natural_key("view_timesheet", "hr", "timesheet")
    can_add_timesheet, is_new = MyPermission.objects.get_or_create_by_natural_key("add_timesheet", "hr", "timesheet")
    can_change_timesheet, is_new = MyPermission.objects.get_or_create_by_natural_key("change_timesheet", "hr", "timesheet")
    can_delete_timesheet, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_timesheet", "hr", "timesheet")
    can_view_expensevoucher, is_new = MyPermission.objects.get_or_create_by_natural_key("view_expensevoucher", "hr", "expensevoucher")
    can_add_expensevoucher, is_new = MyPermission.objects.get_or_create_by_natural_key("add_expensevoucher", "hr", "expensevoucher")
    can_change_expensevoucher, is_new = MyPermission.objects.get_or_create_by_natural_key("change_expensevoucher", "hr", "expensevoucher")
    can_delete_expensevoucher, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_expensevoucher", "hr", "expensevoucher")
    can_view_leaverequest, is_new = MyPermission.objects.get_or_create_by_natural_key("view_leaverequest", "hr", "leaverequest")
    can_add_leaverequest, is_new = MyPermission.objects.get_or_create_by_natural_key("add_leaverequest", "hr", "leaverequest")
    can_change_leaverequest, is_new = MyPermission.objects.get_or_create_by_natural_key("change_leaverequest", "hr", "leaverequest")
    can_delete_leaverequest, is_new = MyPermission.objects.get_or_create_by_natural_key("delete_leaverequest", "hr", "leaverequest")

    hr_link.only_with_perms.add(can_view_timesheet)
    employees_link.only_with_perms.add(can_view_employee)
    timesheets_link.only_with_perms.add(can_view_timesheet)
    expensevouchers_link.only_with_perms.add(can_view_expensevoucher)
    leaverequests_link.only_with_perms.add(can_view_leaverequest)

    employees_group.permissions.add(can_view_timesheet, can_add_timesheet, can_view_expensevoucher, can_add_expensevoucher, can_view_leaverequest, can_add_leaverequest)
    hr_managers_group.permissions.add(can_view_employee, can_add_employee, can_change_employee, can_delete_employee)
    hr_managers_group.permissions.add(can_change_timesheet, can_delete_timesheet)
    hr_managers_group.permissions.add(can_change_expensevoucher, can_delete_expensevoucher)
    hr_managers_group.permissions.add(can_change_leaverequest, can_delete_leaverequest)

post_syncdb.connect(install, dispatch_uid="install_hr")
