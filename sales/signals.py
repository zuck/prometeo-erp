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

from django.db.models.signals import post_save

from prometeo.core.auth.models import ObjectPermission
from prometeo.documents.models import Document

from models import *

## HANDLERS ##

def update_salesinvoice_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the stakeholders of the given sales invoice.
    """
    doc = get_object_or_404(Document.objects.get_for_content(SalesInvoice), object_id=id)

    # Change sales invoice.
    can_change_this_salesinvoice, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_salesinvoice", "sales", "salesinvoice", instance.pk)
    can_change_this_salesinvoice.users.add(doc.author)
    # Delete sales invoice.
    can_delete_this_salesinvoice, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_salesinvoice", "sales", "salesinvoice", instance.pk)
    can_delete_this_salesinvoice.users.add(doc.author)

## CONNECTIONS ##

post_save.connect(update_salesinvoice_permissions, SalesInvoice, dispatch_uid="update_salesinvoice_permissions")
