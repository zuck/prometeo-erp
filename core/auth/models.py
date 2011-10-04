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
__version__ = '0.0.2'

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
 
class UserProfile(models.Model):
    """User profile.
    """
    user = models.OneToOneField(User)
    language = models.CharField(max_length=5, null=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    timezone = models.CharField(max_length=20, null=True, choices=settings.TIME_ZONES, default=settings.TIME_ZONE, verbose_name=_("timezone"))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_("dashboard"))
    bookmarks = models.OneToOneField('menus.Menu', null=True, verbose_name=_("bookmarks"))

