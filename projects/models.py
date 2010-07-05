#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision$'

from django.utils.translation import ugettext_lazy as _
from django.db import models

class Milestone(models.Model):
    project = models.ForeignKey('Project', editable=False, verbose_name=_('project'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'))
    author = models.ForeignKey('auth.User', related_name='created_milestones', editable=False, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_milestones', null=True, blank=True, verbose_name=_('manager'))
    date_due = models.DateTimeField(null=True, blank=True, verbose_name=_('date due'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    date_completed = models.DateTimeField(null=True, blank=True, verbose_name=_('completed on'))

    class Meta:
        ordering = ['-date_due',]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/projects/%d/milestones/view/%d/' % (self.project.id, self.pk)

    def get_edit_url(self):
        return '/projects/%d/milestones/edit/%d/' % (self.project.id, self.pk)

    def get_delete_url(self):
        return '/projects/%d/milestones/delete/%d/' % (self.project.id, self.pk)

    def get_tickets_url(self):
        return self.get_absolute_url() + 'tickets/'
        
    def add_ticket_url(self):
        return '/projects/%d/milestones/%d/tickets/add' % (self.project.id, self.pk)

class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    author = models.ForeignKey('auth.User', related_name='created_projects', editable=False, verbose_name=_('author'))
    pm = models.ForeignKey('auth.User', related_name='managed_projects', null=True, blank=True, verbose_name=_('project manager'))
    members = models.ManyToManyField('auth.User', through='Membership', blank=True, verbose_name=_('members'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    date_closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/projects/view/%d/' % self.pk

    def get_edit_url(self):
        return '/projects/edit/%d/' % self.pk

    def get_delete_url(self):
        return '/projects/delete/%d/' % self.pk

    def get_areas_url(self):
        return self.get_absolute_url() + 'areas/'
        
    def add_area_url(self):
        return '/projects/%d/areas/add' % self.pk

    def get_milestones_url(self):
        return self.get_absolute_url() + 'milestones/'
        
    def add_milestone_url(self):
        return '/projects/%d/milestones/add' % self.pk

    def get_tickets_url(self):
        return self.get_absolute_url() + 'tickets/'

    def add_ticket_url(self):
        return '/projects/%d/tickets/add' % self.pk

    def get_members_url(self):
        return self.get_absolute_url() + 'members/'
        
    def add_member_url(self):
        return '/projects/%d/members/add' % self.pk

    def get_timeline_url(self):
        return self.get_absolute_url() + 'timeline/'
        
    @property
    def project(self):
        return self
        
class Area(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('project'))
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'))
    author = models.ForeignKey('auth.User', related_name='created_areas', editable=False, verbose_name=_('author'))
    manager = models.ForeignKey('auth.User', related_name='managed_areas', null=True, blank=True, verbose_name=_('manager'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    
    def __unicode__(self):
        return _('%(name)s of %(project)s') % {'name': self.name, 'project': self.project}

    def get_absolute_url(self):
        return '/projects/%d/areas/view/%d/' % (self.project.pk, self.pk)

    def get_edit_url(self):
        return '/projects/%d/areas/edit/%d/' % (self.project.pk, self.pk)

    def get_delete_url(self):
        return '/projects/%d/areas/delete/%d/' % (self.project.pk, self.pk)

    def get_tickets_url(self):
        return self.get_absolute_url() + 'tickets/'
        
    def add_ticket_url(self):
        return '/projects/%d/areas/%d/tickets/add' % (self.project.id, self.pk)

class Membership(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_('user'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('joined at'))
    
    def __unicode__(self):
        return "%s" % self.user

    def get_delete_url(self):
        return '/projects/%d/members/delete/%d/' % (self.project.pk, self.pk)

class Ticket(models.Model):
    TICKET_URGENCY_CHOICES = (
        ('low', _('low')),
        ('medium', _('medium')),
        ('high', _('high')),
        ('critical', _('critical')),
    )
    
    TICKET_TYPE_CHOICES = (
        ('defect', _('defect')),
        ('task', _('task')),
        ('enhancement', _('enhancement')),
    )
    
    TICKET_STATUS_CHOICES = (
        ('new', _('new')),
        ('wontfix', _("won't fix")),
        ('duplicate', _('duplicated')),
        ('accepted', _('accepted')),
        ('inprogress', _('in progress')),
        ('resolved', _('resolved')),
        ('review', _('awaiting review')),
    )
    
    project = models.ForeignKey(Project, editable=False, verbose_name=_('project'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    date_closed = models.DateTimeField(null=True, blank=True, verbose_name=_('closed on'))
    date_due = models.DateTimeField(null=True, blank=True, verbose_name=_('date due'))
    area = models.ForeignKey(Area, null=True, blank=True, verbose_name=_('area'))
    milestone = models.ForeignKey(Milestone, null=True, blank=True, verbose_name=_('milestone'))
    author = models.ForeignKey('auth.User', related_name="created_tickets", editable=False, verbose_name=_('author'))
    owners = models.ManyToManyField('auth.User', related_name="assigned_tickets", null=True, blank=True, verbose_name=_('owners'))
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='new', verbose_name=_('status'))
    urgency = models.CharField(max_length=10, choices=TICKET_URGENCY_CHOICES, default='medium', verbose_name=_('urgency'))
    type = models.CharField(max_length=11, choices=TICKET_TYPE_CHOICES, default='defect', verbose_name=_('type'))

    class Meta:
        ordering = ['-date_due', 'id']
        
    def get_absolute_url(self):
        return '/projects/%d/tickets/view/%d/' % (self.project.id, self.id)
        
    def get_edit_url(self):
        return '/projects/%d/tickets/edit/%d/' % (self.project.id, self.id)
        
    def get_delete_url(self):
        return '/projects/%d/tickets/delete/%d/' % (self.project.id, self.id)

    def __unicode__(self):
        for i, t in enumerate(self.project.ticket_set.all()):
            if t == self:
                return u'#%d %s' % (i+1, self.name)
                
        return u''
