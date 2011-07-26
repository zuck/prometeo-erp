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

from django.conf.urls.defaults import *

urlpatterns = patterns('projects.views',

    # Projects.
    url(r'^projects/$', view='projects.project_list', name='project_list'),
    url(r'^projects/add/$', view='projects.project_add', name='project_add'),
    url(r'^projects/(?P<slug>[-\w]+)/$', view='projects.project_detail', name='project_detail'),
    url(r'^projects/(?P<slug>[-\w]+)/edit/$', view='projects.project_edit', name='project_edit'),
    url(r'^projects/(?P<slug>[-\w]+)/delete/$', view='projects.project_delete', name='project_delete'),

    # Areas.
    url(r'^projects/(?P<project>[-\w]+)/areas/$', view='areas.area_list', name='area_list'),
    url(r'^projects/(?P<project>[-\w]+)/areas/add/$', view='areas.area_add', name='area_add'),
    url(r'^projects/(?P<project>[-\w]+)/areas/(?P<slug>[-\w]+)/$', view='areas.area_detail', name='area_detail'),
    url(r'^projects/(?P<project>[-\w]+)/areas/(?P<slug>[-\w]+)/edit/$', view='areas.area_edit', name='area_edit'),
    url(r'^projects/(?P<project>[-\w]+)/areas/(?P<slug>[-\w]+)/delete/$', view='areas.area_delete', name='area_delete'),
    
    # Milestones.
    url(r'^projects/(?P<project>[-\w]+)/milestones/$', view='milestones.milestone_list', name='milestone_list'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/add/$', view='milestones.milestone_add', name='milestone_add'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<slug>[-\w]+)/$', view='milestones.milestone_detail', name='milestone_detail'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<slug>[-\w]+)/edit/$', view='milestones.milestone_edit', name='milestone_edit'),
    url(r'^projects/(?P<project>[-\w]+)/milestones/(?P<slug>[-\w]+)/delete/$', view='milestones.milestone_delete', name='milestone_delete'),

    # Tickets.
    url(r'^projects/(?P<project>[-\w]+)/tickets/$', view='tickets.ticket_list', name='ticket_list'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/add/$', view='tickets.ticket_add', name='ticket_add'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<id>\d+)/$', view='tickets.ticket_detail', name='ticket_detail'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<id>\d+)/edit/$', view='tickets.ticket_edit', name='ticket_edit'),
    url(r'^projects/(?P<project>[-\w]+)/tickets/(?P<id>\d+)/delete/$', view='tickets.ticket_delete', name='ticket_delete'),
)
