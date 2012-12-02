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

from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_save, pre_delete, post_delete

from prometeo.core.auth.signals import *
from prometeo.core.notifications.signals import *

from models import *

## HANDLERS ##

def delete_hard_copy(sender, instance, *args, **kwargs):
    """Deletes the file associated to the given hard copy.
    """
    f = instance.file
    if f:
        f.delete()

## CONNECTIONS ##

post_save.connect(update_author_permissions, Document, dispatch_uid="update_document_permissions")
post_save.connect(update_author_permissions, HardCopy, dispatch_uid="update_hardcopy_permissions")

post_save.connect(notify_object_created, Document, dispatch_uid="document_created")
post_change.connect(notify_object_changed, Document, dispatch_uid="document_changed")
post_delete.connect(notify_object_deleted, Document, dispatch_uid="document_deleted")

post_save.connect(notify_object_created, HardCopy, dispatch_uid="hardcopy_created")
post_delete.connect(notify_object_deleted, HardCopy, dispatch_uid="hardcopy_deleted")
pre_delete.connect(delete_hard_copy, HardCopy, dispatch_uid="delete_hardcopy")

make_observable(Document)
