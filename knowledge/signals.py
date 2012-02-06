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

from prometeo.core.auth.signals import *
from prometeo.core.widgets.signals import *
from prometeo.core.notifications.signals import *

from models import *

## HANDLERS ##

def save_wiki_revision(sender, instance, *args, **kwargs):
    """Saves a revision of the given wiki page.
    """
    if isinstance(instance, WikiPage):
        WikiRevision.objects.create_from_page(instance)

## CONNECTIONS ##

post_save.connect(update_author_permissions, WikiPage, dispatch_uid="update_wikipage_permissions")
post_save.connect(update_author_permissions, Faq, dispatch_uid="update_faq_permissions")
post_save.connect(update_author_permissions, Poll, dispatch_uid="update_poll_permissions")

post_save.connect(save_wiki_revision, WikiPage, dispatch_uid="save_wiki_revision")

post_save.connect(notify_object_created, WikiPage, dispatch_uid="wikipage_created")
post_change.connect(notify_object_changed, WikiPage, dispatch_uid="wikipage_changed")
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
