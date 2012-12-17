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

import re

from django import template

from ..models import *

register = template.Library()

class NotificationForNode(template.Node):
    def __init__(self, instance, var_name, only_unread):
        self.instance = instance
        self.var_name = var_name
        self.only_unread = only_unread

    def render(self, context):
        instance = self.instance.resolve(context)
        notifications = []
        if self.only_unread:
            notifications = Notification.objects.unread_for_object(instance)
        else:
            notifications = Notification.objects.for_object(instance)
        context[self.var_name] = notifications
        return ''

def base_notification_for(parser, token, only_unread=False):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    instance, var_name = m.groups()
    return NotificationForNode(template.Variable(instance), var_name, only_unread)

@register.tag
def notification_for(parser, token):
    return base_notification_for(parser, token)

@register.tag
def unread_notification_for(parser, token):
    return base_notification_for(parser, token, True)
