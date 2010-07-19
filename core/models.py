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
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

class AccountGroup(Group):
    """Group model proxy.
    """
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return '/accounts/groups/view/%d/' % self.pk
        
    def get_edit_url(self):
        return '/accounts/groups/edit/%d/' % self.pk
        
    def get_delete_url(self):
        return '/accounts/groups/delete/%d/' % self.pk
        
    def get_permissions_url(self):
        return self.get_absolute_url() + 'permissions/'

class Account(User):
    """User model proxy.
    """
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return '/accounts/view/%d/' % self.pk
        
    def get_edit_url(self):
        return '/accounts/edit/%d/' % self.pk
        
    def get_delete_url(self):
        return '/accounts/delete/%d/' % self.pk
        
    def get_permissions_url(self):
        return self.get_absolute_url() + 'permissions/'
        
    def get_groups_url(self):
        return self.get_absolute_url() + 'groups/'

class Profile(models.Model):
    """User profile.
    """
    user = models.ForeignKey(User, unique=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))

class ObjectPermission(models.Model):
    """A generic object/row-level permission.
    """
    account = models.ForeignKey(Account)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

def user_post_save(sender, instance, **kwargs):
    profile, new = Profile.objects.get_or_create(user=instance)
    
models.signals.post_save.connect(user_post_save, User)

