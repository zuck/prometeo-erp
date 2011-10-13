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
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
import django.utils.simplejson as json

from prometeo.core.models import validate_json
from prometeo.core.utils import field_to_string

class Observable(object):
    """Mix-in that sends a special signal when a field is changed.
    """
    def __init__(self, *args, **kwargs):
        super(Observable, self).__init__(*args, **kwargs)
        self.__changes = {}
        self.__field_cache = dict([(f.attname, f) for f in (self._meta.fields)])

    def __setattr__(self, name, value):
        try:
            if self.pk and name != 'modified' and name in self.__field_cache:
                field = self.__field_cache[name]
                label = u"%s" % field.verbose_name
                old_value = field_to_string(field, self)
                if label in self.__changes:
                    old_value = self.__changes[label][0]
                super(Observable, self).__setattr__(name, value)
                value = field_to_string(field, self)
                if value != old_value:
                    self.__changes[label] = (u"%s" % old_value, u"%s" % value)
                return
        except AttributeError:
            pass

        super(Observable, self).__setattr__(name, value)

class Stream(models.Model):
    """Stream model.
    """
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    followers = models.ManyToManyField('auth.User', null=True, verbose_name=_('followers'))
    
    class Meta:
        verbose_name = _('stream')
        verbose_name_plural = _('streams')

    def __unicode__(self):
        return self.slug

class Activity(models.Model):
    """Activity model.
    """
    title = models.CharField(_('title'), max_length=200)
    signature = models.CharField(_('signature'), max_length=50)
    template = models.CharField(_('template'), blank=True, null=True, max_length=200, default=None)
    context = models.TextField(_('context'), blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    streams = models.ManyToManyField(Stream, null=True, verbose_name=_('streams'))
    backlink = models.CharField(_('backlink'), blank=True, null=True, max_length=200)
    
    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ('-created',)

    def __unicode__(self):
        try:
            return self.title % self.get_context()
        except:
            return self.title

    def get_context(self):
        try:
            return json.loads(unicode(self.context))
        except:
            return {}

    def get_content(self):
        template_name = "streams/activities/%s.html" % self.signature
        if self.template:
            template_name = self.template
        return render_to_string(template_name, self.get_context())
        
    def get_absolute_url(self):
        if self.backlink:
            return self.backlink
        return ""
