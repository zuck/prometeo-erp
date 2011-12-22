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

from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_save, post_delete

from prometeo.core.widgets.signals import *
from prometeo.core.streams.signals import *
from prometeo.core.streams.models import Activity
from prometeo.core.auth.models import ObjectPermission

from models import *

## UTILS ##

def _get_streams(instance):
    """Returns all available streams for the given object.
    """
    streams = []

    try:
        streams.append(instance.page.stream)
    except:
        pass

    try:
        streams.append(instance.faq.stream)
    except:
        pass

    try:
        streams.append(instance.poll.stream)
    except:
        pass

    try:
        streams.append(instance.stream)
    except:
        pass

    return streams

def _register_followers(instance):
    """Registers all available followers to all available streams.
    """
    for stream in _get_streams(instance):
        try:
            register_follower_to_stream(instance.author, stream)
        except:
            pass

## HANDLERS ##

def update_wikipage_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the stakeholders of the given wiki page.
    """
    # Change wiki page.
    can_change_this_wikipage, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_wikipage", "knowledge", "wikipage", instance.pk)
    can_change_this_wikipage.users.add(instance.author)
    # Delete wiki page.
    can_delete_this_wikipage, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_wikipage", "knowledge", "wikipage", instance.pk)
    can_delete_this_wikipage.users.add(instance.author)

def update_faq_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the stakeholders of the given FAQ.
    """
    # Change FAQ.
    can_change_this_faq, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_faq", "knowledge", "faq", instance.pk)
    can_change_this_faq.users.add(instance.author)
    # Delete FAQ.
    can_delete_this_faq, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_faq", "knowledge", "faq", instance.pk)
    can_delete_this_faq.users.add(instance.author)

def update_poll_permissions(sender, instance, *args, **kwargs):
    """Updates the permissions assigned to the stakeholders of the given poll.
    """
    # Change poll.
    can_change_this_poll, is_new = ObjectPermission.objects.get_or_create_by_natural_key("change_poll", "knowledge", "poll", instance.pk)
    can_change_this_poll.users.add(instance.author)
    # Delete poll.
    can_delete_this_poll, is_new = ObjectPermission.objects.get_or_create_by_natural_key("delete_poll", "knowledge", "poll", instance.pk)
    can_delete_this_poll.users.add(instance.author)

def save_wiki_revision(sender, instance, *args, **kwargs):
    """Saves a revision of the given wiki page.
    """
    if isinstance(instance, WikiPage):
        revision = WikiRevision.objects.create_from_page(instance)

def notify_object_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new object.
    """
    if kwargs['created']:
        _register_followers(instance)

        activity = Activity.objects.create(
            title=_("%(class)s %(name)s created by %(author)s"),
            signature="%s-created" % sender.__name__.lower(),
            template="streams/activities/object-created.html",
            context=json.dumps({
                "class": sender.__name__.lower(),
                "name": "%s" % instance,
                "link": instance.get_absolute_url(),
                "author": "%s" % instance.author,
                "author_link": instance.author.get_absolute_url()
            }),
            backlink=instance.get_absolute_url()
        )

        [activity.streams.add(s) for s in _get_streams(instance)]

def notify_object_change(sender, instance, changes, *args, **kwargs):
    """Generates an activity related to the change of an existing object.
    """
    _register_followers(instance)

    activity = Activity.objects.create(
        title=_("%(class)s %(name)s changed"),
        signature="%s-changed" % sender.__name__.lower(),
        template="streams/activities/object-changed.html",
        context=json.dumps({
            "class": sender.__name__.lower(),
            "name": "%s" % instance,
            "link": instance.get_absolute_url(),
            "changes": changes
        }),
        backlink=instance.get_absolute_url()
    )

    [activity.streams.add(s) for s in _get_streams(instance)]

def notify_object_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing object.
    """
    activity = Activity.objects.create(
        title=_("%(class)s %(name)s deleted"),
        signature="%s-deleted" % sender.__name__.lower(),
        template="streams/activities/object-deleted.html",
        context=json.dumps({
            "class": sender.__name__.lower(),
            "name": "%s" % instance
        }),
    )

    [activity.streams.add(s) for s in _get_streams(instance)]

def notify_comment_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new comment.
    """
    if kwargs['created']:
        obj = instance.content_object

        if isinstance(obj, (WikiPage, Poll)):
            activity = Activity.objects.create(
                title=_("%(author)s commented %(class)s %(name)s"),
                signature="comment-created",
                context=json.dumps({
                    "class": obj.__class__.__name__.lower(),
                    "name": "%s" % obj,
                    "link": instance.get_absolute_url(),
                    "author": "%s" % instance.user,
                    "author_link": instance.user.get_absolute_url(),
                    "comment": instance.comment
                }),
                backlink=obj.get_absolute_url()
            )

            [activity.streams.add(s) for s in _get_streams(obj)]

def notify_comment_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing comment.
    """
    obj = instance.content_object

    activity = Activity.objects.create(
        title=_("comment deleted"),
        signature="comment-deleted",
        context=json.dumps({
            "class": obj.__class__.__name__.lower(),
            "name": "%s" % obj,
            "link": instance.get_absolute_url(),
            "author": "%s" % instance.user,
            "author_link": instance.user.get_absolute_url()
        })
    )

    [activity.streams.add(s) for s in _get_streams(obj)]

def notify_answer_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new answer.
    """
    if kwargs['created']:
        obj = instance.content_object

        if isinstance(obj, Faq):
            activity = Activity.objects.create(
                title=_("%(author)s answered to the %(class)s %(name)s"),
                signature="answer-created",
                template="knowledge/activities/answer-created.html",
                context=json.dumps({
                    "class": obj.__class__.__name__.lower(),
                    "name": "%s" % obj,
                    "link": instance.get_absolute_url(),
                    "author": "%s" % instance.user,
                    "author_link": instance.user.get_absolute_url(),
                    "answer": instance.comment
                }),
                backlink=obj.get_absolute_url()
            )

            [activity.streams.add(s) for s in _get_streams(obj)]

def notify_answer_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing answer.
    """
    obj = instance.content_object

    activity = Activity.objects.create(
        title=_("answer deleted"),
        signature="answer-deleted",
        template="knowledge/activities/answer-deleted.html",
        context=json.dumps({
            "class": obj.__class__.__name__.lower(),
            "name": "%s" % obj,
            "link": instance.get_absolute_url(),
            "author": "%s" % instance.user,
            "author_link": instance.user.get_absolute_url()
        })
    )

    [activity.streams.add(s) for s in _get_streams(obj)]

## CONNECTIONS ##

post_save.connect(update_wikipage_permissions, WikiPage, dispatch_uid="update_wikipage_permissions")
post_save.connect(update_faq_permissions, Faq, dispatch_uid="update_faq_permissions")
post_save.connect(update_poll_permissions, Poll, dispatch_uid="update_poll_permissions")

post_save.connect(save_wiki_revision, WikiPage, dispatch_uid="save_wiki_revision")
post_save.connect(notify_object_created, WikiPage, dispatch_uid="wikipage_created")
post_change.connect(notify_object_change, WikiPage, dispatch_uid="wikipage_changed")
post_delete.connect(notify_object_deleted, WikiPage, dispatch_uid="wikipage_deleted")
post_save.connect(notify_object_created, Faq, dispatch_uid="faq_created")
post_delete.connect(notify_object_deleted, Faq, dispatch_uid="faq_deleted")
post_save.connect(notify_object_created, Poll, dispatch_uid="poll_created")
post_delete.connect(notify_object_deleted, Poll, dispatch_uid="poll_deleted")

#post_save.connect(notify_answer_created, Comment, dispatch_uid="knowledge_answer_created")
#post_delete.connect(notify_answer_deleted, Comment, dispatch_uid="knowledge_answer_deleted")

manage_stream(WikiPage)
manage_stream(Faq)
manage_stream(Poll)

make_observable(WikiPage)
