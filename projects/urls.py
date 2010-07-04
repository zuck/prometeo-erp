#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

from django.conf.urls.defaults import *

urlpatterns = patterns('projects.views',

    # Projects.
    (r'^$', 'project_index'),
    (r'^add/$', 'project_add'),
    (r'^view/(?P<id>\d+)/(?P<page>\w*)/*$', 'project_view'),
    (r'^edit/(?P<id>\d+)/$', 'project_edit'),
    (r'^delete/(?P<id>\d+)/$', 'project_delete'),

    # Areas.
    (r'^(?P<project_id>\d+)/areas/add/$', 'area_add'),
    (r'^(?P<project_id>\d+)/areas/view/(?P<id>\d+)/(?P<page>\w*)/*$', 'area_view'),
    (r'^(?P<project_id>\d+)/areas/edit/(?P<id>\d+)/$', 'area_edit'),
    (r'^(?P<project_id>\d+)/areas/delete/(?P<id>\d+)/$', 'area_delete'),
    (r'^(?P<project_id>\d+)/areas/(?P<id>\d+)/tickets/add/$', 'area_ticket_add'),

    # Milestones.
    (r'^(?P<project_id>\d+)/milestones/add/$', 'milestone_add'),
    (r'^(?P<project_id>\d+)/milestones/view/(?P<id>\d+)/(?P<page>\w*)/*$', 'milestone_view'),
    (r'^(?P<project_id>\d+)/milestones/edit/(?P<id>\d+)/$', 'milestone_edit'),
    (r'^(?P<project_id>\d+)/milestones/delete/(?P<id>\d+)/$', 'milestone_delete'),
    (r'^(?P<project_id>\d+)/milestones/(?P<id>\d+)/tickets/add/$', 'milestone_ticket_add'),

    # Tickets.
    (r'^(?P<project_id>\d+)/tickets/add/$', 'ticket_add'),
    (r'^(?P<project_id>\d+)/tickets/view/(?P<id>\d+)/$', 'ticket_view'),
    (r'^(?P<project_id>\d+)/tickets/edit/(?P<id>\d+)/$', 'ticket_edit'),
    (r'^(?P<project_id>\d+)/tickets/delete/(?P<id>\d+)/$', 'ticket_delete'),

    # Members.
    (r'^(?P<project_id>\d+)/members/add/$', 'member_add'),
    (r'^(?P<project_id>\d+)/members/delete/(?P<id>\d+)/$', 'member_delete'),
)
