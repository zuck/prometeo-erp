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

from django.utils.translation import ugettext_lazy as _

PROJECT_STATUS_CHOICES = (
    ('OPEN', _('open')),
    ('CLOSED', _('closed')),
)

PROJECT_DEFAULT_STATUS = 'OPEN'

PROJECT_CLOSE_STATUSES = ('CLOSED',)

TICKET_URGENCY_CHOICES = (
    ('VERY-LOW', _('very low')),
    ('LOW', _('low')),
    ('MEDIUM', _('medium')),
    ('HIGH', _('high')),
    ('CRITICAL', _('critical')),
)

TICKET_DEFAULT_URGENCY = 'MEDIUM'

TICKET_TYPE_CHOICES = (
    ('BUG', _('bug')),
    ('TASK', _('task')),
    ('IDEA', _('idea')),
)

TICKET_DEFAULT_TYPE = 'BUG'

TICKET_STATUS_CHOICES = (
    ('NEW', _('new')),
    ('TESTS', _('needs tests')),
    ('ACCEPTED', _('accepted')),
    ('INVALID', _("invalid")),
    ('DUPLICATE', _('duplicated')),
    ('RESOLVED', _('resolved')),
    ('REVIEW', _('awaiting review')),
)

TICKET_DEFAULT_STATUS = 'NEW'

TICKET_CLOSE_STATUSES = ('INVALID', 'DUPLICATE', 'RESOLVED')
