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

__author__ = 'Emanuele Bertoldi <zuck@fastwebnet.it>'
__copyright__ = 'Copyright (c) 2010 Emanuele Bertoldi'
__version__ = '$Revision$'

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    """User profile.
    """
    user = models.ForeignKey(User, unique=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))

def user_post_save(sender, instance, **kwargs):
    profile, new = Profile.objects.get_or_create(user=instance)
    
models.signals.post_save.connect(user_post_save, User)

