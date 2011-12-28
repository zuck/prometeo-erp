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

import json

from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_save, post_delete

from prometeo.core.streams.signals import *
from prometeo.core.auth.signals import *

from models import *

## CONNECTIONS ##

post_save.connect(update_author_permissions, Product, dispatch_uid="update_product_permissions")

post_save.connect(notify_object_created, Product, dispatch_uid="product_created")
post_change.connect(notify_object_changed, Product, dispatch_uid="product_changed")
post_delete.connect(notify_object_deleted, Product, dispatch_uid="product_deleted")

post_save.connect(notify_object_created, Supply, dispatch_uid="supply_created")
post_change.connect(notify_object_changed, Supply, dispatch_uid="supply_changed")
post_delete.connect(notify_object_deleted, Supply, dispatch_uid="supply_deleted")

manage_stream(Product)

make_observable(Product)
make_observable(Supply)

manage_dashboard(Product)
