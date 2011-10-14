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

import json

from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_save, post_delete
from django.contrib.comments.models import Comment

from prometeo.core.widgets.signals import *
from prometeo.core.streams.signals import *
from prometeo.core.streams.models import Activity

from models import *

## UTILS ##

def _get_streams(instance):
    """Returns all available streams for the given object.
    """
    streams = []

    if isinstance(instance, Partner):
        streams.append(instance.stream)
    elif isinstance(instance, Contact):
        streams += [p.stream for p in instance.partner_set.all()]
    elif isinstance(instance, Job):
        streams.append(instance.partner.stream)

    return streams

def _register_followers(instance):
    """Registers all available followers to all available streams.
    """
    for stream in _get_streams(instance):
        try:
            register_follower_to_stream(instance.assignee, stream)
        except:
            pass

## HANDLERS ##

def notify_object_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new object.
    """
    if kwargs['created']:
        _register_followers(instance)
        
        title = _("%(class)s %(name)s created")
        signature = "%s-created" % sender.__name__.lower()
        template = "streams/activities/object-created.html"
        context_pairs = {
            "class": sender.__name__.lower(),
            "name": "%s" % instance,
            "link": instance.get_absolute_url()
        }
        backlink = instance.get_absolute_url()

        if isinstance(instance, Partner) and instance.assignee:
            title = _("%(class)s %(name)s created by %(author)s")
            context_pairs.update({
                "author": "%s" % instance.assignee,
                "author_link": instance.assignee.get_absolute_url()
            })

        elif isinstance(instance, Job):
            title = _("Contact added to partner %(partner)s")
            signature = "contact-added"
            template = "partners/activities/contact-added.html"
            context_pairs.update({
                'name':  "%s" % instance.contact,
                'link':  "%s" % instance.contact.get_absolute_url(),
                'partner':  "%s" % instance.partner,
                'partner_link':  "%s" % instance.partner.get_absolute_url(),
                'role':  instance.get_role_display()
            })
            backlink = instance.partner.get_absolute_url()

        activity = Activity.objects.create(
            title=title,
            signature=signature,
            template=template,
            context=json.dumps(context_pairs),
            backlink=backlink
        ) 

        [activity.streams.add(s) for s in _get_streams(instance)]

def notify_object_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing object.
    """
    title = _("%(class)s %(name)s deleted")
    signature = "%s-deleted" % sender.__name__.lower()
    template = "streams/activities/object-deleted.html"
    context_pairs = {
        "class": sender.__name__.lower(),
    }

    if isinstance(instance, Job):
        try:
            title = _("Contact removed from partner %(partner)s")
            signature = "contact-removed"
            template = "partners/activities/contact-removed.html"
            context_pairs.update({
                'name':  "%s" % instance.contact,
                'link':  "%s" % instance.contact.get_absolute_url(),
                'partner':  "%s" % instance.partner,
                'partner_link':  "%s" % instance.partner.get_absolute_url(),
                'role':  instance.get_role_display()
            })
        except:
            return
    else:
        context_pairs.update({"name": "%s" % instance})

    activity = Activity.objects.create(
        title=title,
        signature=signature,
        template=template,
        context=json.dumps(context_pairs)
    )

    [activity.streams.add(s) for s in _get_streams(instance)]

def notify_comment_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new comment.
    """
    if kwargs['created']:
        obj = instance.content_object

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

## CONNECTIONS ##

post_save.connect(notify_object_created, Partner, dispatch_uid="partner_created")
post_delete.connect(notify_object_deleted, Partner, dispatch_uid="partner_deleted")
post_save.connect(notify_object_created, Contact, dispatch_uid="contact_created")
post_delete.connect(notify_object_deleted, Contact, dispatch_uid="contact_deleted")
post_save.connect(notify_object_created, Job, dispatch_uid="contact_added")
post_delete.connect(notify_object_deleted, Job, dispatch_uid="contact_removed")

post_save.connect(notify_comment_created, Comment, dispatch_uid="partners_comment_created")
post_delete.connect(notify_comment_deleted, Comment, dispatch_uid="partners_comment_deleted")

manage_stream(Partner)

manage_dashboard(Partner)
