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

from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save, pre_delete

from prometeo.core.auth.models import ObjectPermission
from prometeo.documents.models import Document
from prometeo.partners.models import Job
from prometeo.core.auth.signals import *

from models import *

## HANDLERS ##

def create_employee(sender, instance, *args, **kwargs):
    """Creates a new employee record for the given job.
    """
    if kwargs['created']:
        employee = Employee.objects.create(job=instance)

def delete_employee(sender, instance, *args, **kwargs):
    """Deletes the employee record related to the given job.
    """
    if instance.employee:
        instance.employee.delete()

def update_employee_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the employee associated with the given document.
    """
    # WARNING: Currently this code doesn't work because the related "Document" instance is saved
    #          AFTER the content object, so when the "post_save" signal is emitted, the document
    #          isn't saved in the database yet:
    """
    doc = Document.objects.get_for_content(sender).get(object_id=instance.pk)

    can_view_this_doc, is_new = ObjectPermission.objects.get_or_create_by_natural_key("view_document", "documents", "document", doc.pk)
    can_change_this_doc, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_document", "documents", "document", doc.pk)
    can_delete_this_doc, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_document", "documents", "document", doc.pk)

    if instance.employee.job.contact.user:
        can_view_this_doc.users.add(instance.employee.job.contact.user)
        can_change_this_doc.users.add(instance.employee.job.contact.user)
        can_delete_this_doc.users.add(instance.employee.job.contact.user)
    """
    pass

## CONNECTIONS ##

post_save.connect(update_author_permissions, Timesheet, dispatch_uid="update_timesheet_permissions")
post_save.connect(update_employee_permissions, Timesheet, dispatch_uid="update_timesheet_employee_permissions")
post_save.connect(update_author_permissions, ExpenseVoucher, dispatch_uid="update_expensevoucher_permissions")
post_save.connect(update_employee_permissions, ExpenseVoucher, dispatch_uid="update_expensevoucher_employee_permissions")

post_save.connect(create_employee, Job, dispatch_uid="create_employee")
pre_delete.connect(delete_employee, Job, dispatch_uid="delete_employee")
