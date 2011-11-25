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

from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from prometeo.core.models import Commentable
from prometeo.core.utils import assign_code

from managers import *

class Project(Commentable):
    """Project model.
    """
    code = models.SlugField(max_length=100, verbose_name=_('code'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_projects', null=True, blank=True, verbose_name=_('created by'))
    manager = models.ForeignKey('auth.User', related_name='managed_projects', null=True, blank=True, verbose_name=_('project manager'))
    status = models.CharField(_('status'), choices=settings.PROJECT_STATUS_CHOICES, default=settings.PROJECT_DEFAULT_STATUS, max_length=10)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_('dashboard'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering = ['code']
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        assign_code(self)

    def __unicode__(self):
        return u'#%s %s' % (self.code, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {"code": self.code})

    @models.permalink
    def get_edit_url(self):
        return ('project_edit', (), {"code": self.code})

    @models.permalink
    def get_delete_url(self):
        return ('project_delete', (), {"code": self.code})

    def save(self):
        if self.status in settings.PROJECT_CLOSE_STATUSES:
            if self.closed is None:
                self.closed = datetime.now()
        else:
            self.closed = None
        super(Project, self).save()

    def working_hours(self):
        count = 0
        for ticket in self.tickets.all():
            count += ticket.working_hours()
        return count

class Milestone(Commentable):
    """Milestone model.
    """
    code = models.SlugField(max_length=100, verbose_name=_('code'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_milestones', null=True, blank=True, verbose_name=_('created by'))
    manager = models.ForeignKey('auth.User', related_name='managed_milestones', null=True, blank=True, verbose_name=_('manager'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('deadline'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_('dashboard'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering = ['project', 'deadline', 'code']
        verbose_name = _('milestone')
        verbose_name_plural = _('milestones')

    def __init__(self, *args, **kwargs):
        super(Milestone, self).__init__(*args, **kwargs)
        assign_code(self)

    def __unicode__(self):
        return u'#%s %s' % (self.code, self.title)
    
    def _expired(self):
        if self.deadline:
            if self.closed:
                return self.closed > self.deadline
            else:
                return datetime.now() > self.deadline
        return False
    expired = property(_expired)
    
    def _progress(self):
        total = self.tickets.count()
        if total > 0:
            closed = self.tickets.closed().count()
            return int(closed / float(total) * 100)
        return 100
    progress = property(_progress)

    @models.permalink
    def get_absolute_url(self):
        return ('milestone_detail', (), {"project": self.project.code, "code": self.code})

    @models.permalink
    def get_edit_url(self):
        return ('milestone_edit', (), {"project": self.project.code, "code": self.code})

    @models.permalink
    def get_delete_url(self):
        return ('milestone_delete', (), {"project": self.project.code, "code": self.code})

    def working_hours(self):
        count = 0
        for ticket in self.tickets.all():
            count += ticket.working_hours()
        return count

class Ticket(Commentable):
    """Ticket model.
    """
    project = models.ForeignKey(Project, related_name='tickets', verbose_name=_('project'))
    code = models.PositiveIntegerField(verbose_name=_('code'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(help_text=_('Use <a href="http://daringfireball.net/projects/markdown/syntax">MarkDown syntax</a>.'), verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name="created_tickets", verbose_name=_('created by'))
    milestone = models.ForeignKey(Milestone, null=True, blank=True, related_name='tickets', on_delete=models.SET_NULL, verbose_name=_('milestone'))
    type = models.CharField(max_length=11, choices=settings.TICKET_TYPE_CHOICES, default=settings.TICKET_DEFAULT_TYPE, verbose_name=_('type'))
    urgency = models.CharField(max_length=10, choices=settings.TICKET_URGENCY_CHOICES, default=settings.TICKET_DEFAULT_URGENCY, verbose_name=_('urgency'))
    status = models.CharField(max_length=10, choices=settings.TICKET_STATUS_CHOICES, default=settings.TICKET_DEFAULT_STATUS, verbose_name=_('status'))
    assignee = models.ForeignKey('auth.User', related_name="assigned_tickets", null=True, blank=True, verbose_name=_('assigned to'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    tasks = models.ManyToManyField('todo.Task', null=True, blank=True, verbose_name=_('related tasks'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    objects = TicketManager()     

    class Meta:
        ordering = ('project', '-code')
        permissions = (
            ("change_assignee", "Can change assignee"),
        )
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)
        if not self.code:
            uid = 1
            try:
                last_ticket = Ticket.objects.filter(project=self.project).latest('created')
                uid = int(last_ticket.code) + 1
            except:
                pass
            self.code = uid

    def __unicode__(self):
        return u'#%d %s' % (self.code, self.title)
    
    @models.permalink    
    def get_absolute_url(self):
        return ('ticket_detail', (), {"project": self.project.code, "code": self.code})
    
    @models.permalink    
    def get_edit_url(self):
        return ('ticket_edit', (), {"project": self.project.code, "code": self.code})
    
    @models.permalink    
    def get_delete_url(self):
        return ('ticket_delete', (), {"project": self.project.code, "code": self.code})
        
    def save(self):
        if self.status in settings.TICKET_CLOSE_STATUSES:
            if self.closed is None:
                self.closed = datetime.now()
        else:
            self.closed = None
        super(Ticket, self).save()

    def working_hours(self):
        count = 0
        for task in self.tasks.all():
            count += task.working_hours()
        return count
