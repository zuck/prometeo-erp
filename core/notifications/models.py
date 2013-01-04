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

import hashlib, json
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string

from prometeo.core.models import validate_json
from prometeo.core.utils import field_to_string

from managers import *

class FollowRelation(models.Model):
    """FollowRelation model.
    """
    followed_content_type = models.ForeignKey(ContentType, related_name="+")
    followed_id = models.PositiveIntegerField()
    followed = generic.GenericForeignKey('followed_content_type', 'followed_id')
    follower_content_type = models.ForeignKey(ContentType, related_name="+")
    follower_id = models.PositiveIntegerField()
    follower = generic.GenericForeignKey('follower_content_type', 'follower_id')

    objects = GFKManager()
    
    class Meta:
        verbose_name = _('follow relation')
        verbose_name_plural = _('follow relations')

    def __unicode__(self):
        return _("%s followed by %s") % (self.followed, self.follower)

class Signature(models.Model):
    """Signature model.
    """
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('signature')
        verbose_name_plural = _('signatures')

    def __unicode__(self):
        return self.title
        
class Subscription(models.Model):
    """Subscription model.
    """
    subscriber_content_type = models.ForeignKey(ContentType, related_name="+")
    subscriber_id = models.PositiveIntegerField()
    subscriber = generic.GenericForeignKey('subscriber_content_type', 'subscriber_id')
    signature = models.ForeignKey(Signature)
    send_email = models.BooleanField(default=True, verbose_name=_('send email'))
    email = models.EmailField(null=True, blank=True, verbose_name=_('email'))

    objects = GFKManager()

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __unicode__(self):
        return "%s | %s" % (self.subscriber, self.signature)

class Activity(models.Model):
    """Activity model.
    """
    title = models.CharField(_('title'), max_length=200)
    signature = models.CharField(_('signature'), max_length=50)
    template = models.CharField(_('template'), blank=True, null=True, max_length=200, default=None)
    context = models.TextField(_('context'), blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    backlink = models.CharField(_('backlink'), blank=True, null=True, max_length=200)
    source_content_type = models.ForeignKey(ContentType, related_name="+")
    source_id = models.PositiveIntegerField()
    source = generic.GenericForeignKey('source_content_type', 'source_id')

    objects = ActivityManager()
    
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
    target_content_type = models.ForeignKey(ContentType, related_name="+")
    target_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_content_type', 'target_id')
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
        if self.target:
            return ('notification_detail', (), {"object_model": self.target._meta.verbose_name_plural, "object_id": self.target.pk, "id": self.pk})
        return None

    @models.permalink
    def get_delete_url(self):
        if self.target:
            return ('notification_delete', (), {"object_model": self.target._meta.verbose_name_plural, "object_id": self.target.pk, "id": self.pk})
        return None

    def clean(self):
        if not Subscription.objects.filter(subscriber=self.target, signature=self.signature):
            raise ValidationError('The target is not subscribed for this kind of notification.')
        super(Notification, self).clean()

    def save(self, *args, **kwargs):
        if self.dispatch_uid is None:
            self.dispatch_uid = hashlib.md5(self.title + self.description + datetime.now()).hexdigest()
        super(Notification, self).save(*args, **kwargs)

class Observable(object):
    """Mix-in that sends a special signal when a field is changed.
    """
    def __init__(self, *args, **kwargs):
        super(Observable, self).__init__(*args, **kwargs)
        self.__changes = {}
        self.__field_cache = dict([(f.attname, f) for f in (self._meta.fields)])
        self.__followers_cache = None

    def __setattr__(self, name, value):
        try:
            if self.pk and name in self.__field_cache:
                field = self.__field_cache[name]
                label = u"%s" % field.verbose_name
                if name not in self.__change_exclude:
                    old_value = field_to_string(field, self)
                    if label in self.__changes:
                        old_value = self.__changes[label][0]
                    super(Observable, self).__setattr__(name, value)
                    value = field_to_string(field, self)
                    if value != old_value:
                        self.__changes[label] = (u"%s" % old_value, u"%s" % value)
                return

        except:
            pass
        
        super(Observable, self).__setattr__(name, value)

    def followers(self):
        """Returns the list of the current followers.
        """
        if self.__followers_cache:
            return self.__followers_cache
        return [r.follower for r in FollowRelation.objects.filter(followed=self)]

    def follow(self, followers):
        """Registers the given followers.
        """
        if not isinstance(followers, (tuple, list)):
            followers = [followers]

        for f in followers:
            if not isinstance(f, models.Model):
                continue

            r = FollowRelation.objects.get_or_create(follower=f, followed=self)

    def unfollow(self, followers):
        """Unregisters the given followers.
        """
        if not isinstance(followers, (tuple, list)):
            followers = [followers]

        for f in followers:
            if not isinstance(f, models.Model):
                continue

            FollowRelation.objects.filter(follower=f, followed=self).delete()

class NotificationTarget(object):
    """Mix-in that adds some useful methods to retrieve related notifications.
    """
    def _notification_set(self):
        return Notification.objects.for_object(self)
    notification_set = property(_notification_set)
