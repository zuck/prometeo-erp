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

from django.core.urlresolvers import reverse
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    knowledge_menu, is_new = Menu.objects.get_or_create(
        slug="knowledge_menu",
        description=_("Main menu for knowledge app")
    )

    wikipage_menu, is_new = Menu.objects.get_or_create(
        slug="wikipage_menu",
        description=_("Main menu for a wiki page")
    )

    faq_menu, is_new = Menu.objects.get_or_create(
        slug="faq_menu",
        description=_("Main menu for a FAQ")
    )

    poll_menu, is_new = Menu.objects.get_or_create(
        slug="poll_menu",
        description=_("Main menu for a poll")
    )
    
    # Links.
    knowledge_link, is_new = Link.objects.get_or_create(
        title=_("Knowledge"),
        slug="knowledge",
        description=_("Knowledge management"),
        url=reverse("wikipage_home"),
        submenu=knowledge_menu,
        menu=main_menu
    )

    wiki_link, is_new = Link.objects.get_or_create(
        title=_("Wiki"),
        slug="wiki",
        description=_("Wiki home"),
        url=reverse("wikipage_home"),
        menu=knowledge_menu
    )

    faq_link, is_new = Link.objects.get_or_create(
        title=_("FAQs"),
        slug="faq",
        description=_("Frequently Asked Questions"),
        url=reverse("faq_list"),
        menu=knowledge_menu
    )

    polls_link, is_new = Link.objects.get_or_create(
        title=_("Polls"),
        slug="polls",
        description=_("Polls"),
        url=reverse("poll_list"),
        menu=knowledge_menu
    )

    wikipage_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="wikipage_details",
        url="{{ object.get_absolute_url }}",
        menu=wikipage_menu
    )

    wikipage_revisions_link, is_new = Link.objects.get_or_create(
        title=_("Revisions"),
        slug="wikipage_revisions",
        url="{% url wikipage_revisions object.slug %}",
        menu=wikipage_menu
    )

    wikipage_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="wikipage_timeline",
        url="{% url wikipage_timeline object.slug %}",
        menu=wikipage_menu
    )

    faq_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="faq_details",
        url="{{ object.get_absolute_url }}",
        menu=faq_menu
    )

    faq_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="faq_timeline",
        url="{% url faq_timeline object.pk %}",
        menu=faq_menu
    )

    poll_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="poll_details",
        url="{{ object.get_absolute_url }}",
        menu=poll_menu
    )

    poll_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="poll_timeline",
        url="{% url poll_timeline object.pk %}",
        menu=poll_menu
    )

    # Signatures.
    wikipage_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Wiki page created"),
        slug="wikipage-created"
    )

    wikipage_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Wiki page changed"),
        slug="wikipage-changed"
    )

    wikipage_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Wiki page deleted"),
        slug="wikipage-deleted"
    )

    faq_created_signature, is_new = Signature.objects.get_or_create(
        title=_("FAQ created"),
        slug="faq-created"
    )

    faq_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("FAQ deleted"),
        slug="faq-deleted"
    )

    answer_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Answer created"),
        slug="answer-created"
    )

    answer_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Answer deleted"),
        slug="answer-deleted"
    )

    poll_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Poll created"),
        slug="poll-created"
    )

    poll_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Poll deleted"),
        slug="poll-deleted"
    )

    poll_closed_signature, is_new = Signature.objects.get_or_create(
        title=_("Poll closed"),
        slug="poll-closed"
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)
