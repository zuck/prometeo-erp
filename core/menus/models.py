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
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Permission
from django.db.models import permalink
        
class Menu(models.Model):
    """Menu model.
    """
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def __unicode__(self):
        return self.slug

class Link(models.Model):
    """A generic menu entry.
    """
    menu = models.ForeignKey(Menu, db_column='menu_id', related_name='links', verbose_name=_('menu'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    url = models.CharField(max_length=200, verbose_name=_('url'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    new_window = models.BooleanField(default=False, verbose_name=_('New window?'))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_('sort order'))
    submenu = models.ForeignKey(Menu, db_column='submenu_id', related_name='parent_links', blank=True, null=True, verbose_name=_('sub-menu'))
    only_authenticated = models.BooleanField(default=True, verbose_name=_('Only for authenticated users'))
    only_staff = models.BooleanField(default=False, verbose_name=_('Only for staff users'))
    only_with_perms = models.ManyToManyField(Permission, blank=True, null=True, verbose_name=_('Only with following permissions'))

    class Meta:
        ordering = ('menu', 'sort_order', 'id',)
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __unicode__(self):
        return '%s | %s' % (self.menu, self.title)

    def get_absolute_url(self):
        if self.url.startswith('www.'):
            return "http://" + self.url
        return self.url

class Bookmark(Link):
    """A proxy model for bookmark links.
    """
    class Meta:
        proxy = True
        verbose_name = _('bookmark')
        verbose_name_plural = _('bookmarks')

    def __unicode__(self):
        return '%s' % self.title
        
    @models.permalink
    def get_edit_url(self):
        user = get_object_or_404(User, pk=self.slug.split('_')[1])
        return ('bookmark_edit', (), {"username": user.username, "slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        user = get_object_or_404(User, pk=self.slug.split('_')[1])
        return ('bookmark_delete', (), {"username": user.username, "slug": self.slug})
