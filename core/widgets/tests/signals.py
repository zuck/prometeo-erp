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

from ..models import *
from ..signals import *

class DashboardTestPseudoModel(object):
    def __init__(self, pk):
        self.dashboard = None
        self.pk = pk

    def save(self):
        pass

class RegionTestCase(unittest.TestCase):
    def test_dashboard(self):
        d = DashboardTestPseudoModel(1)
        self.assertEqual(d.dashboard, None)
        create_dashboard(DashboardTestPseudoModel, d)
        self.assertTrue(isinstance(d.dashboard, Region))
        self.assertEqual(d.dashboard.slug, "dashboardtestpseudomodel_1_dashboard")
        delete_dashboard(DashboardTestPseudoModel, d)
        self.assertEqual(Region.objects.filter(slug="dashboardtestpseudomodel_1_dashboard").count(), 0)
        self.assertEqual(d.dashboard, None)

    def test_unique_dashboard(self):
        d1 = DashboardTestPseudoModel(1)
        create_dashboard(DashboardTestPseudoModel, d1)
        self.assertEqual(d1.dashboard.slug, "dashboardtestpseudomodel_1_dashboard")
        d2 = DashboardTestPseudoModel(1)
        create_dashboard(DashboardTestPseudoModel, d2)
        self.assertEqual(d2.dashboard.slug, "dashboardtestpseudomodel_1_dashboard")
        self.assertEqual(d1.dashboard, d2.dashboard)
