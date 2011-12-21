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
from django.utils.translation import ugettext_noop as _
import django.dispatch

from prometeo.core.notifications.models import *

from models import *

## UTILS ##

def register_follower_to_stream(follower, stream):
    """Registers the given follower to the given stream.
    """
    if follower and follower not in stream.followers.all():
        stream.followers.add(follower)

def manage_stream(cls):
    """Connects handlers for stream management.
    """
    models.signals.pre_save.connect(create_stream, cls)
    models.signals.post_save.connect(update_stream, cls)
    models.signals.post_delete.connect(delete_stream, cls)

def make_observable(cls):
    """Adds Observable mix-in to the given class.
    """
    if Observable not in cls.__bases__:
        cls.__bases__ += (Observable,)
    models.signals.post_save.connect(notify_changes, sender=cls, dispatch_uid="%s_notify_changes" % cls.__name__)

## HANDLERS ##

def notify_changes(sender, instance, *args, **kwargs):
    """Notifies one or more changes in an Observable-derived model.
    
    Changes are notified sending a "post_change" signal.
    """
    if not kwargs['created']:
        try:
            changes = {}
            for name, (old_value, value) in instance._Observable__changes.items():
                if value != old_value:
                    changes[name] = (old_value, value)  
            instance._Observable__changes = {}
            if changes:
                post_change.send(sender=sender, instance=instance, changes=changes)
        except AttributeError:
            pass

def forward_activity(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Forwards a new activity to all the linked streams.
    """
    print sender, instance, action, reverse, model, pk_set

    if not isinstance(instance, Activity):
        return

    if action == "post_add":
        for stream_id in pk_set:
            stream = Stream.objects.get(id=stream_id)
            for s in stream.linked_streams.all():
                s.activity_set.add(instance)            

def notify_activity(sender, instance, action, *args, **kwargs):
    """Notifies a new activity to all the followers of the related streams.
    """
    if not isinstance(instance, Activity):
        return

    activity = instance
    content = activity.get_content()

    # Notifies an activity to all the followers.
    if action == "post_add":
        subscriptions = Subscription.objects.filter(signature__slug=activity.signature).distinct()
        streams = activity.streams.all()
        for subscription in subscriptions:
            for stream in streams:
                if subscription.user in stream.followers.all():
                    notification, is_new = Notification.objects.get_or_create(
                        signature=subscription.signature,
                        user=subscription.user,
                        description=content,
                        title=u"%s" % activity,
                        dispatch_uid="%d" % activity.id,
                    )
                    break

    # Deletes orphans.
    elif action in ["post_remove", "post_clear"]:
        streams = activity.streams.all()
        if len(streams) == 0:
            activity.delete()

def clear_orphans(sender, instance, *args, **kwargs):
    """Clears all orphan activites.
    """
    if not isinstance(instance, Stream):
        return

    # Deletes orphans.
    for activity in instance.activity_set.all():
        streams = activity.streams.all()
        if len(streams) == 1 and streams[0] == instance:
            activity.delete()

def create_stream(sender, instance, *args, **kwargs):
    """Creates a new stream for the given object.
    """
    if not instance.stream:
        instance.stream = Stream.objects.create(slug="%s_stream" % sender.__name__.lower())

def update_stream(sender, instance, *args, **kwargs):
    """Updates the slug field of the object's stream.
    """
    stream = instance.stream
    if stream:
        stream.slug = "%s_%d_stream" % (sender.__name__.lower(), instance.pk)
        stream.save()

def delete_stream(sender, instance, *args, **kwargs):
    """Deletes the stream of the given object.
    """
    stream = instance.stream
    if stream:
        stream.delete()

## SIGNALS ##

post_change = django.dispatch.Signal(providing_args=["instance", "changes"])

## CONNECTIONS ##

models.signals.m2m_changed.connect(forward_activity, sender=Activity.streams.through, dispatch_uid="forward_activities")
models.signals.m2m_changed.connect(notify_activity, sender=Activity.streams.through, dispatch_uid="change_activities")
models.signals.pre_delete.connect(clear_orphans, sender=Stream, dispatch_uid="clear_orphans")
