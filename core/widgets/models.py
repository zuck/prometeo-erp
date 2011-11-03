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
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def __unicode__(self):
        return self.slug

class Widget(models.Model):
    """Widget model.
    """
    region = models.ForeignKey(Region, related_name='widgets')
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    source = models.CharField(_('source'), blank=False, null=False, max_length=200)
    template = models.CharField(_('template'), blank=True, null=True, max_length=200, default="widgets/widget.html")
    context = models.TextField(_('context'), blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'))
    show_title = models.BooleanField(_('show title'), default=True)
    editable = models.BooleanField(_('editable'), default=False)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)

    class Meta:
        ordering = ('sort_order', 'title',)
        verbose_name = _('widget')
        verbose_name_plural = _('widgets')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_edit_url(self):
        return ('widget_edit', (), {"slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        return ('widget_delete', (), {"slug": self.slug})
