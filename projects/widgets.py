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

from django.db.models import Q

from models import Project, Milestone, Ticket

def my_projects(context):
    user = context['user']
    context['project_list'] = Project.objects.filter(Q(author=user) | Q(manager=user))
    return context

def my_latest_tickets(context):
    user = context['user']
    try:
        count = context['count']
    except KeyError:
        count = 5
    context['ticket_list'] = Ticket.objects.filter(Q(author=user) | Q(assignee=user))[0:count]
    return context

def latest_tickets(context):
    try:
        count = context['count']
    except KeyError:
        count = 5
    try:
        obj = context['object']
        try:
            context['ticket_list'] = obj.tickets.all()[0:count]
        except AttributeError:
            context['ticket_list'] = obj.ticket_set.all()[0:count]
        if isinstance(obj, Project):
            context['project'] = obj
        elif isinstance(obj, Milestone):
            context['milestone'] = obj
    except:
        context['ticket_list'] = None
    return context
