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

from django.utils.functional import lazy

from models import *

# ObjPermWrapper and ObjPermLookupDict proxy the permissions system into objects
# that the template system can understand.

class ObjPermLookupDict(object):
    def __init__(self, user, module_name):
        self.user, self.module_name = user, module_name

    def __repr__(self):
        return str([p for p in self.user.get_all_permissions() if len(p.split('.')) == 3])

    def __getitem__(self, perm_name):
        if self.user.is_superuser:
            perms = Permission.objects.filter(content_type__app_label=self.module_name, codename=perm_name)
            return [obj.pk for p in perms for obj in p.content_type.model_class().objects.all()]
        return [p.object_id for p in self.user.objectpermissions.filter(perm__content_type__app_label=self.module_name, perm__codename=perm_name)]

    def __nonzero__(self):
        if self.user.is_superuser:
            return True
        return self.user.objectpermissions.filter(perm__contentype__app_label=self.module_name).exists()


class ObjPermWrapper(object):
    def __init__(self, user):
        self.user = user

    def __getitem__(self, module_name):
        return ObjPermLookupDict(self.user, module_name)

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("ObjPermWrapper is not iterable.")

def auth(request):
    """
    Returns context variables required by apps that use Prometeo's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    # If we access request.user, request.session is accessed, which results in
    # 'Vary: Cookie' being sent in every request that uses this context
    # processor, which can easily be every request on a site if
    # TEMPLATE_CONTEXT_PROCESSORS has this context processor added.  This kills
    # the ability to cache.  So, we carefully ensure these attributes are lazy.
    # We don't use django.utils.functional.lazy() for User, because that
    # requires knowing the class of the object we want to proxy, which could
    # break with custom auth backends.  LazyObject is a less complete but more
    # flexible solution that is a good enough wrapper for 'User'.
    def get_user():
        if hasattr(request, 'user'):
            return request.user
        else:
            from django.contrib.auth.models import AnonymousUser
            return AnonymousUser()

    return {
        'obj_perms':  lazy(lambda: ObjPermWrapper(get_user()), ObjPermWrapper)(),
    }
