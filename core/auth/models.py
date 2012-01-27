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
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from managers import *

class MyUser(User):
    """A Prometeo's user.
    """
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        self._meta.get_field('is_active').verbose_name = _('active?')
        self._meta.get_field('is_staff').verbose_name = _('staff?')
        self._meta.get_field('is_superuser').verbose_name = _('admin?')

    def _full_name(self):
        return self.get_full_name()
    _full_name.short_description = _('full name')
    full_name = property(_full_name)
    
    @models.permalink
    def get_edit_url(self):
        return ('user_edit', (), {"username": self.username})
    
    @models.permalink
    def get_delete_url(self):
        return ('user_delete', (), {"username": self.username})

class MyPermission(Permission):
    """A Prometeo's permission.
    """ 
    class Meta:
        proxy = True

    objects = MyPermissionManager()
 
class UserProfile(models.Model):
    """User profile.
    """
    user = models.OneToOneField(User)
    language = models.CharField(max_length=5, null=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    timezone = models.CharField(max_length=20, null=True, choices=settings.TIME_ZONES, default=settings.TIME_ZONE, verbose_name=_("timezone"))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_("dashboard"))
    bookmarks = models.OneToOneField('menus.Menu', null=True, verbose_name=_("bookmarks"))
    calendar = models.OneToOneField('calendar.Calendar', null=True, verbose_name=_("calendar"))
    
    def __unicode__(self):
        return self.user.username

class ObjectPermission(models.Model):
    """A generic object/row-level permission.
    """
    object_id = models.PositiveIntegerField()
    perm = models.ForeignKey(Permission, verbose_name=_("permission"))
    users = models.ManyToManyField(User, null=True, blank=True, related_name='objectpermissions', verbose_name=_("users"))
    groups = models.ManyToManyField(Group, null=True, blank=True, related_name='objectpermissions', verbose_name=_("groups"))

    objects = ObjectPermissionManager()

    class Meta:
        verbose_name = _('object permission')
        verbose_name_plural = _('object permissions')

    def __unicode__(self):
        return "%s | %d" % (self.perm, self.object_id)
