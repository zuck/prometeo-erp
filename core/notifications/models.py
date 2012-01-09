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

import hashlib
from datetime import datetime

from django.db import models
import django.utils.simplejson as json
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from prometeo.core.models import validate_json
from prometeo.core.utils import field_to_string

from managers import *

class Observable(object):
    """Mix-in that sends a special signal when a field is changed.
    """
    def __init__(self, *args, **kwargs):
        super(Observable, self).__init__(*args, **kwargs)
        self.__changes = {}
        self.__field_cache = dict([(f.attname, f) for f in (self._meta.fields)])

    def __setattr__(self, name, value):
        try:
            if self.pk and name in self.__field_cache:
                field = self.__field_cache[name]
                label = u"%s" % field.verbose_name
                if label not in self.__change_exclude:
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

class Signature(models.Model):
    """Signature model.
    """
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    subscribers = models.ManyToManyField('auth.User', null=True, blank=True, through='Subscription', verbose_name=_('subscribers'))

    class Meta:
        verbose_name = _('signature')
        verbose_name_plural = _('signatures')

    def __unicode__(self):
        return self.title
        
class Subscription(models.Model):
    """Subscription model.
    """
    user = models.ForeignKey('auth.User')
    signature = models.ForeignKey(Signature)
    send_email = models.BooleanField(default=True, verbose_name=_('send email'))

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

class Stream(models.Model):
    """Stream model.
    """
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    linked_streams = models.ManyToManyField('self', null=True, blank=True, symmetrical=False, verbose_name=_('linked streams'))
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
        template_name = "notifications/activities/%s.html" % self.signature
        if self.template:
            template_name = self.template
        return render_to_string(template_name, self.get_context())
        
    def get_absolute_url(self):
        if self.backlink:
            return self.backlink
        return ""

class Notification(models.Model):
    """Notification model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    signature = models.ForeignKey(Signature, verbose_name=_('signature'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    read = models.DateTimeField(blank=True, null=True, verbose_name=_('read on'))
    dispatch_uid = models.CharField(max_length=32, verbose_name=_('dispatch UID'))

    objects = NotificationManager()

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ('-created', 'id')
        get_latest_by = '-created'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('notification_detail', (), {"username": self.user.username, "id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('notification_delete', (), {"username": self.user.username, "id": self.pk})

    def clean(self):
        if self.user.subscription_set.filter(signature=self.signature).count() == 0:
            raise ValidationError('The user is not subscribed for this kind of notification.')
        super(Notification, self).clean()

    def save(self, *args, **kwargs):
        if self.dispatch_uid is None:
            self.dispatch_uid = hashlib.md5(self.title + self.description + datetime.now()).hexdigest()
        super(Notification, self).save(*args, **kwargs)
