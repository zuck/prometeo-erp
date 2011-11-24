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

from django.conf.urls.defaults import *

urlpatterns = patterns('knowledge.views',

    # Wiki pages.
    url(r'^wiki/$', view='wiki.page_list', name='wikipage_home'),
    url(r'^wiki/add/$', view='wiki.page_edit', name='wikipage_add'),
    url(r'^wiki/(?P<slug>[-\w]+)/$', view='wiki.page_detail', name='wikipage_detail'),
    url(r'^wiki/(?P<slug>[-\w]+)/edit/$', view='wiki.page_edit', name='wikipage_edit'),
    url(r'^wiki/(?P<slug>[-\w]+)/delete/$', view='wiki.page_delete', name='wikipage_delete'),
    url(r'^wiki/(?P<slug>[-\w]+)/revisions/$', view='wiki.page_revisions', name='wikipage_revisions'),
    url(r'^wiki/(?P<slug>[-\w]+)/revisions/(?P<created>.+)/$', view='wiki.page_revision_detail', name='wikipage_revision_detail'),
    url(r'^wiki/(?P<slug>[-\w]+)/timeline/$', 'wiki.page_detail', {'template_name': 'knowledge/wikipage_timeline.html'}, 'wikipage_timeline'),

    # FAQ.
    url(r'^faq/$', view='faq.faq_list', name='faq_list'),
    url(r'^faq/add/$', view='faq.faq_add', name='faq_add'),
    url(r'^faq/(?P<id>\d+)/$', view='faq.faq_detail', name='faq_detail'),
    url(r'^faq/(?P<id>\d+)/edit$', view='faq.faq_edit', name='faq_edit'),
    url(r'^faq/(?P<id>\d+)/delete$', view='faq.faq_delete', name='faq_delete'),

    # Polls.
    url(r'^polls/$', view='polls.poll_list', name='poll_list'),
    url(r'^polls/add/$', view='polls.poll_add', name='poll_add'),
    url(r'^polls/(?P<id>\d+)/$', view='polls.poll_detail', name='poll_detail'),
    url(r'^polls/(?P<id>\d+)/edit/$', view='polls.poll_edit', name='poll_edit'),
    url(r'^polls/(?P<id>\d+)/delete/$', view='polls.poll_delete', name='poll_delete'),
    url(r'^polls/(?P<id>\d+)/vote/(?P<choice>\d+)/$', view='polls.poll_vote', name='poll_vote'),
)
