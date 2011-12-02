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
from django.utils.translation import ugettext_lazy as _

from prometeo.core.models import validate_json
    
class Region(models.Model):
    """Region model.
    """
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def __unicode__(self):
        return self.slug

class Widget(models.Model):
    """Widget model.
    """
    region = models.ForeignKey(Region, related_name='widgets', verbose_name=_('region'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    source = models.CharField(blank=False, null=False, max_length=200, verbose_name=_('source'))
    template = models.CharField(blank=True, null=True, max_length=200, default="widgets/widget.html", verbose_name=_('template'))
    context = models.TextField(blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'), verbose_name=_('context'))
    show_title = models.BooleanField(default=True, verbose_name=_('show title'))
    editable = models.BooleanField(default=False, verbose_name=_('editable'))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_('sort order'))

    class Meta:
        ordering = ('region', 'sort_order', 'title',)
        verbose_name = _('widget')
        verbose_name_plural = _('widgets')

    def __unicode__(self):
        return u"%s | %s" % (self.region, self.title)

    @models.permalink
    def get_edit_url(self):
        return ('widget_edit', (), {"slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        return ('widget_delete', (), {"slug": self.slug})
