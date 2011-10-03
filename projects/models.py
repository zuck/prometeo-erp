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

import datetime

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from prometeo.core.models import Commentable

from managers import *

class Project(Commentable):
    """Project model.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_projects', null=True, blank=True, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_projects', null=True, blank=True, verbose_name=_('project manager'))
    status = models.CharField(_('status'), choices=settings.PROJECT_STATUS_CHOICES, default='opened', max_length=10)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_("dashboard"))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_("stream"))

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {"slug": self.slug})

    @models.permalink
    def get_edit_url(self):
        return ('project_edit', (), {"slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        return ('project_delete', (), {"slug": self.slug})

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save()

class Milestone(Commentable):
    """Milestone model.
    """
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_milestones', null=True, blank=True, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_milestones', null=True, blank=True, verbose_name=_('manager'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('deadline'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_("dashboard"))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_("stream"))

    class Meta:
        ordering = ['deadline', 'created']

    def __unicode__(self):
        return u'%s' % self.title
    
    def _expired(self):
        if self.deadline:
            if self.closed:
                return self.closed > self.deadline
            else:
                return datetime.datetime.now() > self.deadline
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
        return ('milestone_detail', (), {"project": self.project.slug, "slug": self.slug})

    @models.permalink
    def get_edit_url(self):
        return ('milestone_edit', (), {"project": self.project.slug, "slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        return ('milestone_delete', (), {"project": self.project.slug, "slug": self.slug})
        
    def save(self):
        if not self.slug:
            self.slug = slugify('%s_%s' % (self.project.pk, self.title))
        super(Milestone, self).save()  

class Ticket(Commentable):
    """Ticket model.
    """    
    project = models.ForeignKey(Project, related_name='tickets', verbose_name=_('project'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name="created_tickets", verbose_name=_('author'))
    milestone = models.ForeignKey(Milestone, null=True, blank=True, related_name='tickets', verbose_name=_('milestone'))
    type = models.CharField(max_length=11, choices=settings.TICKET_TYPE_CHOICES, default='bug', verbose_name=_('type'))
    urgency = models.CharField(max_length=10, choices=settings.TICKET_URGENCY_CHOICES, default='medium', verbose_name=_('urgency'))
    status = models.CharField(max_length=10, choices=settings.TICKET_STATUS_CHOICES, default='new', verbose_name=_('status'))
    assignee = models.ForeignKey('auth.User', related_name="assigned_tickets", null=True, blank=True, verbose_name=_('assignee'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_("stream"))

    objects = TicketManager()     

    class Meta:
        ordering = ('created', 'id')
        get_latest_by = 'created'
        permissions = (
            ("change_assignee", "Can change assignee"),
        )

    def __unicode__(self):
        return u'#%d %s' % (self.pk, self.title)
    
    @models.permalink    
    def get_absolute_url(self):
        return ('ticket_detail', (), {"project": self.project.slug, "id": self.pk})
    
    @models.permalink    
    def get_edit_url(self):
        return ('ticket_edit', (), {"project": self.project.slug, "id": self.pk})
    
    @models.permalink    
    def get_delete_url(self):
        return ('ticket_delete', (), {"project": self.project.slug, "id": self.pk})
        
    def save(self):
        if self.status in ('invalid', 'duplicated', 'resolved'):
            if self.closed is None:
                self.closed = datetime.datetime.now()
        else:
            self.closed = None
        super(Ticket, self).save()
