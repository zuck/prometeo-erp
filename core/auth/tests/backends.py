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

from django.utils import unittest

from prometeo.core.auth.backends import *

class ObjectPermissionBackendTestCase(unittest.TestCase):
    def test_has_perm(self):
        b = ObjectPermissionBackend()
        p = Permission.objects.get_by_natural_key("delete_user", "auth", "user")
        p_name = "auth.delete_user"
        u = User.objects.get(username="u")
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")
        u1.user_permissions.add(p)
        op = ObjectPermission.objects.create(object_id=u.pk, perm=p)
        op.users.add(u2)
        self.assertFalse(b.has_perm(u1, p, u))
        self.assertTrue(b.has_perm(u2, p, u))
        self.assertFalse(b.has_perm(u, p, u))
        self.assertFalse(b.has_perm(u, p_name, u))
        self.assertTrue(b.has_perm(u2, p_name, u))
        self.assertFalse(b.has_perm(u, p_name, u))
