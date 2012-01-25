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

from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _
from django.contrib.auth.models import Group

from prometeo.core.auth.models import MyPermission
from prometeo.core.utils import check_dependency

check_dependency('prometeo.core.auth')

def install(sender, **kwargs):
    # Groups.
    administrative_employees_group, is_new = Group.objects.get_or_create(
        name=_('Administrative Employees')
    )

    # Permissions.
    can_add_address, is_new = MyPermission.objects.get_or_create_by_natural_key("add_address", "addressing", "address")
    can_add_phonenumber, is_new = MyPermission.objects.get_or_create_by_natural_key("add_phonenumber", "addressing", "phonenumber")
    can_add_socialprofile, is_new = MyPermission.objects.get_or_create_by_natural_key("add_socialprofile", "addressing", "socialprofile")

    administrative_employees_group.permissions.add(can_add_address, can_add_phonenumber, can_add_socialprofile)

post_syncdb.connect(install, dispatch_uid="install_addressing")
