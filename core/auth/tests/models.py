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
from django.contrib.auth.models import User

from prometeo.core.auth.models import *

class MyUserTestCase(unittest.TestCase):
    def test_proxy(self):
        u = MyUser.objects.create(username="u", password="test", email="u@test.it")
        self.assertEqual(isinstance(u, MyUser), True)
        self.assertEqual(issubclass(MyUser, User), True)

    def test_full_name(self):
        u1 = MyUser.objects.create(username="u1", password="test", email="u1@test.it")
        self.assertEqual(u1.full_name, "")
        u2 = MyUser.objects.create(username="u2", password="test", first_name="John", last_name="Doe", email="u2@test.it")
        self.assertEqual(u2.full_name, "John Doe")
        self.assertEqual(u2.full_name, u2.get_full_name())
