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

    try:
        streams.append(instance.stream)
        streams.append(instance.project.stream)
        streams.append(instance.milestone.stream)
    except:
        pass

    return streams

def _register_followers(instance):
    """Registers all available followers to all available streams.
    """
    for stream in _get_streams(instance):
        try:
            register_follower_to_stream(instance.author, stream)
            register_follower_to_stream(instance.manager, stream)
            register_follower_to_stream(instance.assignee, stream)
        except:
            pass

## HANDLERS ##

def notify_object_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new object.
    """
    if kwargs['created']:
        _register_followers(instance)

        activity = Activity.objects.create(
            title=_("%(class)s %(name)s created by %(author)s"),
            description=_('%(class)s <a href="%(link)s">%(name)s</a> has been created by <a href="%(author_link)s">%(author)s</a>.'),
            signature="%s-created" % (sender.__name__.lower()),
            context='{"class": "%s", "name": "%s", "link": "%s", "author": "%s", "author_link": "%s"}' % (
                sender.__name__.lower(),
                instance,
                instance.get_absolute_url(),
                instance.author,
                instance.author.get_absolute_url()
            ),
            backlink=instance.get_absolute_url()
        )

        [activity.streams.add(s) for s in _get_streams(instance)]

def notify_object_change(sender, instance, changes, *args, **kwargs):
    """Generates an activity related to the change of an existing object.
    """
    _register_followers(instance)

    activity = Activity.objects.create(
        title=_("%(class)s %(name)s changed"),
        description=_('The following attributes of %(class)s <a href="%(link)s">%(name)s</a> has been changed:<br/>%(changes)s'),
        signature="%s-changed" % (sender.__name__.lower()),
        context='{"class": "%s", "name": "%s", "link": "%s", "changes": "%s"}' % (
            sender.__name__.lower(),
            instance,
            instance.get_absolute_url(),
            changes
        ),
        backlink=instance.get_absolute_url()
    )

    [activity.streams.add(s) for s in _get_streams(instance)]

def notify_object_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing object.
    """
    activity = Activity.objects.create(
        title=_("%(class)s %(name)s deleted"),
        description=_('%(class)s %(name)s has been deleted.'),
        signature="%s-deleted" % (sender.__name__.lower()),
        context='{"class": "%s", "name": "%s"}' % (
            sender.__name__.lower(),
            instance,
        )
    )

    [activity.streams.add(s) for s in _get_streams(instance)]

def notify_comment_created(sender, instance, *args, **kwargs):
    """Generates an activity related to the creation of a new comment.
    """
    if kwargs['created']:
        obj = instance.content_object

        if isinstance(obj, (Project, Milestone, Ticket)):
            activity = Activity.objects.create(
                title=_("%(author)s commented %(class)s %(name)s"),
                description=_('<a href="%(author_link)s">%(author)s</a> has posted a comment to %(class)s <a href="%(link)s">%(name)s</a>:<br/>%(comment)s'),
                signature="comment-created",
                context='{"class": "%s", "name": "%s", "link": "%s", "author": "%s", "author_link": "%s", "comment": "%s"}' % (
                    obj.__class__.__name__.lower(),
                    obj,
                    obj.get_absolute_url(),
                    instance.user_name,
                    instance.user.get_absolute_url(),
                    instance.comment
                ),
                backlink=obj.get_absolute_url()
            )

            [activity.streams.add(s) for s in _get_streams(obj)]

def notify_comment_deleted(sender, instance, *args, **kwargs):
    """Generates an activity related to the deletion of an existing comment.
    """
    obj = instance.content_object

    activity = Activity.objects.create(
        title=_("comment deleted"),
        description=_('A comment of <a href="%(author_link)s">%(author)s</a> has been deleted from %(class)s <a href="%(link)s">%(name)s</a>.'),
        signature="comment-deleted",
        context='{"class": "%s", "name": "%s", "link": "%s", "author": "%s", "author_link": "%s"}' % (
            obj.__class__.__name__.lower(),
            obj,
            obj.get_absolute_url(),
            instance.user_name,
            instance.user.get_absolute_url(),
        )
    )

    [activity.streams.add(s) for s in _get_streams(obj)]

## CONNECTIONS ##

post_save.connect(notify_object_created, Project, dispatch_uid="project_created")
post_change.connect(notify_object_change, Project, dispatch_uid="project_changed")
post_delete.connect(notify_object_deleted, Project, dispatch_uid="project_deleted")
post_save.connect(notify_object_created, Milestone, dispatch_uid="milestone_created")
post_change.connect(notify_object_change, Milestone, dispatch_uid="milestone_changed")
post_delete.connect(notify_object_deleted, Milestone, dispatch_uid="milestone_deleted")
post_save.connect(notify_object_created, Ticket, dispatch_uid="ticket_created")
post_change.connect(notify_object_change, Ticket, dispatch_uid="ticket_changed")
post_delete.connect(notify_object_deleted, Ticket, dispatch_uid="ticket_deleted")

post_save.connect(notify_comment_created, Comment, dispatch_uid="projects_comment_created")
post_delete.connect(notify_comment_deleted, Comment, dispatch_uid="projects_comment_deleted")

manage_stream(Project)
manage_stream(Milestone)
manage_stream(Ticket)

manage_dashboard(Project)
manage_dashboard(Milestone)

make_observable(Project)
make_observable(Milestone)
make_observable(Ticket)
