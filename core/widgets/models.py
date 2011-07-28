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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import django.utils.simplejson as json

from prometeo.core.auth.models import *
        
def validate_json(value):
    try:
        json.loads(value)
    except:
        raise ValidationError('Ivalid JSON syntax')
    
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
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)

    class Meta:
        ordering = ('sort_order', 'title',)
        verbose_name = _('widget')
        verbose_name_plural = _('widgets')

    def __unicode__(self):
        return self.title

def profile_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.dashboard:
        dashboard = Region(slug="profile_%d_dashboard" % instance.pk, description='Dashboard')
        dashboard.save()
        instance.dashboard = dashboard
        instance.save()

def profile_post_delete(sender, instance, signal, *args, **kwargs):
    dashboard = instance.dashboard
    if dashboard:
        dashboard.delete()

models.signals.post_save.connect(profile_post_save, UserProfile)
models.signals.post_delete.connect(profile_post_delete, UserProfile)
