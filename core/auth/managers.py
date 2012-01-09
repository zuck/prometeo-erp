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
from django.db.models import Q, get_model, get_models, get_app
from django.contrib.auth.models import Permission, PermissionManager
from django.contrib.contenttypes.models import ContentType

class MyPermissionManager(PermissionManager):
    """Custom manager for Permission model.
    """
    def get_or_create_by_natural_key(self, codename, app_label, model):
        get_models(get_app(app_label))
        ct = ContentType.objects.get_for_model(get_model(app_label, model))
        action, sep, model_name = codename.rpartition('_')
        name = "Can %s %s" % (action.replace('_', ' '), ct.name)
        return Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)

class ObjectPermissionManager(models.Manager):
    """Custom manager for ObjectPermission model.
    """
    def get_by_natural_key(self, codename, app_label, model, object_id):
        perm = Permission.objects.get_by_natural_key(codename, app_label, model)
        return self.get(perm=perm, object_id=object_id)

    def get_or_create_by_natural_key(self, codename, app_label, model, object_id):
        perm, is_new = MyPermissionManager().get_or_create_by_natural_key(codename, app_label, model)
        return self.get_or_create(perm=perm, object_id=object_id)

    def get_group_permissions(self, user):
        return self.filter(groups__user=user)

    def get_all_permissions(self, user):
        return self.filter(Q(groups__user=user) | Q(users=user))
