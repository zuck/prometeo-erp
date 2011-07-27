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
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment

from prometeo.core import models as prometeo_models

class Project(prometeo_models.Commentable):
    PROJECT_STATUS_CHOICES = (
        ('opened', _('opened')),
        ('closed', _('closed')),
    )

    title = models.CharField(max_length=100, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_projects', null=True, blank=True, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_projects', null=True, blank=True, verbose_name=_('project manager'))
    status = models.CharField(_('status'), choices=PROJECT_STATUS_CHOICES, default='opened', max_length=10)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    
    def _milestones(self):
        """Returns only the top-level milestones.
        """
        return self.milestone_set.filter(parent=None)
    milestones = property(_milestones)

    def _areas(self):
        """Returns only the top-level areas.
        """
        return self.area_set.filter(parent=None)
    areas = property(_areas)

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {"slug": self.slug})
        
class Area(prometeo_models.Commentable):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_areas', null=True, blank=True, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_areas', null=True, blank=True, verbose_name=_('manager'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    
    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('area_detail', (), {"project": self.project.slug, "slug": self.slug})

class Milestone(prometeo_models.Commentable):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    parent = models.ForeignKey('self', related_name='sub_milestones', null=True, blank=True, verbose_name=_('parent'))
    author = models.ForeignKey('auth.User', related_name='created_milestones', null=True, blank=True, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_milestones', null=True, blank=True, verbose_name=_('manager'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    date_due = models.DateTimeField(null=True, blank=True, verbose_name=_('date due'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    
    def _expired(self):
        if self.date_due:
            if self.closed:
                return self.closed > self.date_due
            else:
                return datetime.datetime.now() > self.date_due
        return False
    expired = property(_expired)
    
    def _progress(self):
        total = self.tickets.count()
        if total > 0:
            closed = self.tickets.closed().count()
            return int(closed / float(total) * 100)
        return 100
    progress = property(_progress)

    class Meta:
        ordering = ['-date_due',]

    @models.permalink
    def get_absolute_url(self):
        return ('milestone_detail', (), {"project": self.project.slug, "slug": self.slug})
        
    def save(self):
        if self.date_due:
            if self.parent != None:
                if self.parent.date_due and self.date_due > self.parent.date_due:
                    self.date_due = self.parent.date_due
            else:
                for child in self.sub_milestones.all():
                    if child.date_due and child.date_due > self.date_due:
                        child.date_due = self.date_due
        super(Milestone, self).save()
        for child in self.sub_milestones.all():
            child.save()

    def __unicode__(self):
        return u'%s' % self.title
        
class TicketManager(models.Manager):
    
    def opened(self):
        return self.filter(closed=None)
    
    def closed(self):
        return self.exclude(closed=None)
    
    def last(self):
        return self.opened()[:5]
    

class Ticket(prometeo_models.Commentable):
    TICKET_URGENCY_CHOICES = (
        ('very low', _('very low')),
        ('low', _('low')),
        ('medium', _('medium')),
        ('high', _('high')),
        ('critical', _('critical')),
    )
    
    TICKET_TYPE_CHOICES = (
        ('bug', _('bug')),
        ('task', _('task')),
        ('idea', _('idea')),
    )
    
    TICKET_STATUS_CHOICES = (
        ('new', _('new')),
        ('tests', _('needs tests')),
        ('accepted', _('accepted')),
        ('invalid', _("invalid")),
        ('duplicate', _('duplicated')),
        ('resolved', _('resolved')),
        ('review', _('awaiting review')),
    )
    
    project = models.ForeignKey(Project, related_name='tickets', verbose_name=_('project'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name="created_tickets", verbose_name=_('author'))
    last_modified_by = models.ForeignKey('auth.User', related_name="modified_tickets", editable=False, null=True, blank=True, verbose_name=_('last modified by'))
    areas = models.ManyToManyField(Area, null=True, blank=True, verbose_name=_('areas'))
    milestone = models.ForeignKey(Milestone, null=True, blank=True, related_name='tickets', verbose_name=_('milestone'))
    type = models.CharField(max_length=11, choices=TICKET_TYPE_CHOICES, default='bug', verbose_name=_('type'))
    urgency = models.CharField(max_length=10, choices=TICKET_URGENCY_CHOICES, default='medium', verbose_name=_('urgency'))
    assignees = models.ManyToManyField('auth.User', related_name="assigned_tickets", null=True, blank=True, verbose_name=_('assignees'))
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='new', verbose_name=_('status'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified on'))
    closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    public = models.BooleanField(_('public'), default=True)

    objects = TicketManager()
    
    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)
        self.__changes = {}      

    class Meta:
        ordering = ('created', 'id')
        get_latest_by = 'created'
        
    def __setattr__(self, name, value):
        try:
            if self.pk and name != 'modified' and name in [f.attname for f in self._meta.fields]:
                old_value = getattr(self, name)
                if value != old_value:
                    self.__changes[name] = (old_value, value)
        except AttributeError:
            pass
        super(Ticket, self).__setattr__(name, value)
        
    def save(self):
        if self.status in ('invalid', 'duplicated', 'resolved'):
            if self.closed is None:
                self.closed = datetime.datetime.now()
        else:
            self.closed = None
        super(Ticket, self).save()
        reports = []
        for name, (old_value, value) in self.__changes.items():
            if old_value:
                reports.append(u'**%s**' % name)
        if reports:      
            body = u'Changed %s.' % (u', '.join(reports))
            data = {
                'content_object': self,
                'comment': body,
                'submit_date': datetime.datetime.now(),
                'site': Site.objects.get_current(), 
                'user': self.last_modified_by,
            }
            try:
                data['user_name'] = self.last_modified_by.username
                data['user_email'] = self.last_modified_by.email
            except:
                pass
            Comment.objects.create(**data)
        self.__changes = {}
    
    @models.permalink    
    def get_absolute_url(self):
        return ('ticket_detail', (), {"project": self.project.slug, "id": self.pk})

    def __unicode__(self):
        return u'#%d %s' % (self.pk, self.title)
