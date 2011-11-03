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

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Permission

class ObjectPermissionManager(models.Manager):
    """Custom manager for ObjectPermission model.
    """
    def get_by_natural_key(self, codename, app_label, model, object_id):
        perm = Permission.objects.get_by_natural_key(codename, app_label, model)
        return self.get(perm=perm, object_id=object_id)

    def get_or_create_by_natural_key(self, codename, app_label, model, object_id):
        perm = Permission.objects.get_by_natural_key(codename, app_label, model)
        return self.get_or_create(perm=perm, object_id=object_id)

    def get_group_permissions(self, user):
        return self.filter(groups__user=user)

    def get_all_permissions(self, user):
        return self.filter(Q(groups__user=user) | Q(users=user))
