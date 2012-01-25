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

from django.conf import settings
from django.contrib.auth.models import User

from models import *

class ObjectPermissionBackend(object):
    """Backend which enables support for row-level permissions.
    """
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        return None

    def get_group_permissions(self, user_obj):
        if not hasattr(user_obj, '_group_obj_perm_cache'):
            perms = ObjectPermission.objects.get_group_permissions(user_obj)
            perms = perms.values_list('perm__content_type__app_label', 'perm__codename', 'object_id').order_by()
            user_obj._group_obj_perm_cache = set(["%s.%s.%s" % (ct, name, obj_id) for ct, name in perms])
        return user_obj._group_obj_perm_cache

    def get_all_permissions(self, user_obj):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_obj_perm_cache'):
            user_obj._obj_perm_cache = set([u"%s.%s.%s" % (p.perm.content_type.app_label, p.perm.codename, p.object_id) for p in user_obj.objectpermissions.all()])
            user_obj._obj_perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._obj_perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        """This method checks if the user_obj has perm on obj.
        """
        if not user_obj.is_authenticated():
            user_obj = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

        if user_obj.is_superuser:
            return True

        if not user_obj.is_active:
            return False

        if obj is None:
            return False

        if isinstance(perm, Permission):
            perm = "%s.%s" % (perm.content_type.app_label, perm.codename)

        return "%s.%d" % (perm, obj.pk) in self.get_all_permissions(user_obj)
