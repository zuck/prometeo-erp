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

import django.dispatch
from django.db import models
from django.utils.translation import ugettext_noop as _
from django.core.mail import EmailMessage
from django.contrib.comments.models import Comment
from django.conf import settings

from prometeo.core.auth.models import ObjectPermission
from prometeo.core.auth.cache import LoggedInUserCache
from prometeo.core.notifications.models import *

from models import *

## UTILS ##

def register_follower_to_stream(follower, stream):
    """Registers the given follower to the given stream(s).
    """
    if follower:
        try:
            [s.followers.add(follower) for s in stream]
        except:
            stream.followers.add(follower)

def register_activity_to_stream(activity, stream):
    """Registers the given activity to the given stream(s).
    """
    try:
        [activity.streams.add(s) for s in stream]
    except:
        activity.streams.add(stream)

def manage_stream(cls):
    """Connects handlers for stream management.
    """
    models.signals.post_save.connect(create_stream, cls, dispatch_uid="%s_stream_creation" % cls.__name__)
    models.signals.post_delete.connect(delete_stream, cls, dispatch_uid="%s_stream_deletion" % cls.__name__)

def make_observable(cls, exclude=['stream_id', 'dashboard_id', 'modified']):
    """Adds Observable mix-in to the given class.
    """
    if Observable not in cls.__bases__:
        class _Observable(Observable):
            __change_exclude = exclude
        cls.__bases__ += (_Observable,)
    models.signals.post_save.connect(notify_changes, sender=cls, dispatch_uid="%s_notify_changes" % cls.__name__)

## HANDLERS ##

def notify_object_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new object.
    """
    if kwargs['created']:
        create_stream(sender, instance)

        try:            
            stream = kwargs.get('stream', instance.stream)

            author = LoggedInUserCache().current_user
            title = _("%(class)s %(name)s created")
            context = {
                "class": sender.__name__.lower(),
                "name": "%s" % instance,
                "link": instance.get_absolute_url(),
            }

            register_follower_to_stream(author, stream)

            if author:
                title = _("%(class)s %(name)s created by %(author)s")
                context.update({
                    "author": "%s" % author,
                    "author_link": author.get_absolute_url()
                })

            activity = Activity.objects.create(
                title=title,
                signature="%s-created" % sender.__name__.lower(),
                template="notifications/activities/object-created.html",
                context=json.dumps(context),
                backlink=instance.get_absolute_url()
            )

            register_activity_to_stream(activity, stream)

        except:
            pass

def notify_object_changed(sender, instance, changes, *args, **kwargs):
    """Generates an activity related to the change of an existing object.
    """
    create_stream(sender, instance)

    try:            
        stream = kwargs.get('stream', instance.stream)

        author = LoggedInUserCache().current_user
        title = _("%(class)s %(name)s changed")
        context = {
            "class": sender.__name__.lower(),
            "name": "%s" % instance,
            "link": instance.get_absolute_url(),
            "changes": changes
        }

        register_follower_to_stream(author, stream)

        if author:
            title = _("%(class)s %(name)s changed by %(author)s")
            context.update({
                "author": "%s" % author,
                "author_link": author.get_absolute_url()
            })

        activity = Activity.objects.create(
            title=title,
            signature="%s-changed" % sender.__name__.lower(),
            template="notifications/activities/object-changed.html",
            context=json.dumps(context),
            backlink=instance.get_absolute_url()
        )

        register_activity_to_stream(activity, stream)

    except:
        pass

def notify_object_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing object.
    """
    create_stream(sender, instance)

    try:            
        stream = kwargs.get('stream', instance.stream)

        author = LoggedInUserCache().current_user
        title = _("%(class)s %(name)s deleted")
        context = {
            "class": sender.__name__.lower(),
            "name": "%s" % instance
        }

        register_follower_to_stream(author, stream)

        if author:
            title = _("%(class)s %(name)s deleted by %(author)s")
            context.update({
                "author": "%s" % author,
                "author_link": author.get_absolute_url()
            })

        activity = Activity.objects.create(
            title=title,
            signature="%s-deleted" % sender.__name__.lower(),
            template="notifications/activities/object-deleted.html",
            context=json.dumps(context)
        )

        register_activity_to_stream(activity, stream)

    except:
        pass

def notify_m2m_changed(sender, instance, action, reverse, model, pk_set, *args, **kwargs):
    """Generates one or more activities related to the change of an existing many-to-many relationship.
    """
    create_stream(sender, instance)

    try:            
        stream = kwargs.get('stream', instance.stream)

        if action == "post_add":
            for pk in pk_set:
                notify_object_created(sender=model, instance=model.objects.get(pk=pk), stream=stream)

        elif action == "post_remove":
            for pk in pk_set:
                notify_object_deleted(sender=model, instance=model.objects.get(pk=pk), stream=stream)

    except:
        pass

def notify_comment_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new comment.
    """
    if kwargs['created']:
        obj = instance.content_object

        create_stream(obj.__class__, obj)

        try:            
            stream = obj.stream

            author = instance.user or LoggedInUserCache().current_user

            register_follower_to_stream(author, stream)

            activity = Activity.objects.create(
                title=_("%(author)s commented %(class)s %(name)s"),
                signature="comment-created",
                context=json.dumps({
                    "class": obj.__class__.__name__.lower(),
                    "name": "%s" % obj,
                    "link": instance.get_absolute_url(),
                    "author": "%s" % author,
                    "author_link": author.get_absolute_url(),
                    "comment": instance.comment
                }),
                backlink=obj.get_absolute_url()
            )

            register_activity_to_stream(activity, stream)

        except:
            pass

def notify_comment_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing comment.
    """
    obj = instance.content_object

    create_stream(obj.__class__, obj)

    try:            
        stream = obj.stream

        author = LoggedInUserCache().current_user or instance.user

        register_follower_to_stream(author, stream)

        activity = Activity.objects.create(
            title=_("comment deleted by %(author)s"),
            signature="comment-deleted",
            context=json.dumps({
                "class": obj.__class__.__name__.lower(),
                "name": "%s" % obj,
                "link": instance.get_absolute_url(),
                "author": "%s" % author,
                "author_link": author.get_absolute_url()
            })
        )

        register_activity_to_stream(activity, stream)

    except:
        pass

def notify_changes(sender, instance, **kwargs):
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
    if hasattr(instance, "stream") and not instance.stream:
        stream, is_new = Stream.objects.get_or_create(slug="%s_%d_stream" % (sender.__name__.lower(), instance.pk))
        if not is_new:
            for a in stream.activities.all():
                a.delete()
        stream_attach.send(sender=sender, instance=instance, stream=stream)
        instance.stream = stream
        instance.save()

def delete_stream(sender, instance, *args, **kwargs):
    """Deletes the stream of the given object.
    """
    stream = instance.stream
    if stream:
        stream.delete()
        instance.stream = None

def send_notification_email(sender, instance, signal, *args, **kwargs):
    if Subscription.objects.filter(signature=instance.signature, user=instance.user, send_email=True).count() > 0:
        email_subject = instance.title
        email_body = instance.description
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
        email = EmailMessage(email_subject, email_body, email_from, [instance.user.email,])
        email.content_subtype = "html"
        email.send()

## SIGNALS ##

post_change = django.dispatch.Signal(providing_args=["instance", "changes"])
stream_attach = django.dispatch.Signal(providing_args=["instance", "stream"])

## CONNECTIONS ##

models.signals.m2m_changed.connect(forward_activity, sender=Activity.streams.through, dispatch_uid="forward_activities")
models.signals.m2m_changed.connect(notify_activity, sender=Activity.streams.through, dispatch_uid="notify_activities")
models.signals.pre_delete.connect(clear_orphans, sender=Stream, dispatch_uid="clear_orphans")

models.signals.post_save.connect(notify_comment_created, Comment, dispatch_uid="comment_created")
models.signals.post_delete.connect(notify_comment_deleted, Comment, dispatch_uid="comment_deleted")

models.signals.post_save.connect(send_notification_email, Notification)
