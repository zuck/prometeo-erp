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
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.conf import settings

from prometeo.core.auth.models import MyPermission, ObjectPermission
from prometeo.core.auth.cache import LoggedInUserCache

from models import *

## HANDLERS ##

def update_user_permissions(sender, instance, *args, **kwargs):
    """Sets permissions for notifications management.
    """
    if kwargs['created']:
        can_view_notification, is_new = MyPermission.objects.get_or_create_by_natural_key("view_notification", "notifications", "notification")
        instance.user_permissions.add(can_view_notification)

def notify_object_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new object.
    """
    if kwargs['created']:
        try:
            author = LoggedInUserCache().current_user
            title = _("%(class)s %(name)s created")
            context = {
                "class": sender.__name__.lower(),
                "name": "%s" % instance,
                "link": instance.get_absolute_url(),
            }

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
                backlink=instance.get_absolute_url(),
                source=instance
            )

        except:
            pass

def notify_object_changed(sender, instance, changes, *args, **kwargs):
    """Generates an activity related to the change of an existing object.
    """
    try:
        author = LoggedInUserCache().current_user
        title = _("%(class)s %(name)s changed")
        context = {
            "class": sender.__name__.lower(),
            "name": "%s" % instance,
            "link": instance.get_absolute_url(),
            "changes": changes
        }

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
            backlink=instance.get_absolute_url(),
            source=instance
        )

    except:
        pass

def notify_object_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing object.
    """
    try:
        author = LoggedInUserCache().current_user
        title = _("%(class)s %(name)s deleted")
        context = {
            "class": sender.__name__.lower(),
            "name": "%s" % instance
        }

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
            context=json.dumps(context),
            source=instance
        )

    except:
        pass

def notify_m2m_changed(sender, instance, action, reverse, model, pk_set, *args, **kwargs):
    """Generates one or more activities related to the change of an existing many-to-many relationship.
    """
    try:
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

        try:
            author = instance.user or LoggedInUserCache().current_user

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
                backlink=obj.get_absolute_url(),
                source=obj
            )

        except:
            pass

def notify_comment_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing comment.
    """
    obj = instance.content_object

    try:
        author = LoggedInUserCache().current_user or instance.user

        activity = Activity.objects.create(
            title=_("comment deleted by %(author)s"),
            signature="comment-deleted",
            context=json.dumps({
                "class": obj.__class__.__name__.lower(),
                "name": "%s" % obj,
                "link": instance.get_absolute_url(),
                "author": "%s" % author,
                "author_link": author.get_absolute_url()
            }),
            source=obj
        )

    except:
        pass

def notify_changes(sender, instance, **kwargs):
    """Notifies one or more changes in an Observable-derived model.
    
    Changes are notified sending a "post_change" signal.
    """
    if issubclass(sender, Observable):

        if kwargs['created']:
            print "Created! %s %d" % (instance, instance.pk)
            instance.follow(instance)
            for sf in instance._Observable__subscriber_fields:
                if hasattr(instance, sf):
                    follower = getattr(instance, sf)
                    instance.follow(follower)

        else:
            changes = {}
            for name, (old_value, value) in instance._Observable__changes.items():
                if value != old_value:
                    changes[name] = (old_value, value)
                    if name in instance._Observable__subscriber_fields:
                        instance.unfollow(old_value)
                        instance.follow(value)
            instance._Observable__changes = {}
            if changes:
                post_change.send(sender=sender, instance=instance, changes=changes)

def notify_activity(sender, instance, created, raw, using, **kwargs):
    """Notifies a new activity to all the followers of the related object.
    """
    if not isinstance(instance, Activity):
        return

    # Notifies an activity to all the followers.
    if created:
        source = instance.source
        content = instance.get_content()
        signature = Signature.objects.get(slug=instance.signature)
        followers = source.followers()
        subscribers = [s.subscriber for s in Subscription.objects.filter(signature=signature).distinct()]
        print followers # REMOVE ME!
        for follower in followers:
            # NOTE: Don't change "==" to "is".
            if (follower == source) or (follower in subscribers):
                notification, is_new = Notification.objects.get_or_create(
                    title=u"%s" % instance,
                    description=content,
                    target=follower,
                    signature=signature,
                    dispatch_uid="%d" % instance.pk,
                )

def send_notification_email(sender, instance, signal, *args, **kwargs):
    """Sends an email related to the notification.
    """
    if Subscription.objects.filter(signature=instance.signature, subscriber=instance.target, send_email=True).count() > 0:
        email_subject = instance.title
        email_body = instance.description
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
        try:
            email = EmailMessage(email_subject, email_body, email_from, [instance.target.email,])
            email.content_subtype = "html"
            email.send()
        except:
            pass

## SIGNALS ##

post_change = django.dispatch.Signal(providing_args=["instance", "changes"])

## UTILS ##

def make_observable(cls, exclude=['stream_id', 'dashboard_id', 'modified'], subscriber_fields=['parent', 'author']):
    """Adds Observable mix-in to the given class.

    Should be placed before every other signal connection for the given class.

    @param cls The object class which needs to be observed.
    @param exclude The list of fields to not track in changes.
    @param subscriber_fields The list of fields which represent subscribers models.
    """
    if not issubclass(cls, Observable):

        class _Observable(Observable):
            __change_exclude = exclude
            __subscriber_fields = subscriber_fields

        cls.__bases__ += (_Observable,)

        models.signals.post_save.connect(notify_changes, sender=cls, dispatch_uid="%s_notify_changes" % cls.__name__)

def make_notification_target(cls):
    """Adds NotificationTarget mix-in to the given class.

    @param cls The object class.
    """
    if not issubclass(cls, NotificationTarget):
        cls.__bases__ += (NotificationTarget,)

## CONNECTIONS ##

models.signals.post_save.connect(notify_activity, sender=Activity, dispatch_uid="notify_activity")
models.signals.post_save.connect(send_notification_email, Notification, dispatch_uid="send_notification_email")

models.signals.post_save.connect(update_user_permissions, sender=User, dispatch_uid="update_user_permissions")

models.signals.post_save.connect(notify_comment_created, Comment, dispatch_uid="comment_created")
models.signals.post_delete.connect(notify_comment_deleted, Comment, dispatch_uid="comment_deleted")

make_notification_target(User)
