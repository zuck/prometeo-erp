#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class TimeLine(models.Model):
    project = models.ForeignKey('Project', editable=False)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return _(u'(<a href="%(link)s">%(object)s</a>) %(description)s on %(date)s') % {'link':self.content_object.get_absolute_url, 'object':self.content_object, 'description':self.description, 'date':self.date}

    class Meta:
        ordering = ('-date',)

class Milestone(models.Model):
    project = models.ForeignKey('Project', editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    creator = models.ForeignKey('auth.User', related_name='created_milestones', editable=False)
    manager = models.ForeignKey('auth.User', related_name='managed_milestones', null=True, blank=True)
    date_due = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)

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
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey('auth.User', related_name='created_projects', editable=False)
    pm = models.ForeignKey('auth.User', related_name='managed_projects', verbose_name=_('Project manager'), null=True, blank=True)
    members = models.ManyToManyField('auth.User', through='Membership', blank=True)
    events = generic.GenericRelation(TimeLine, related_name='projects')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

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
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    creator = models.ForeignKey('auth.User', related_name='created_areas', editable=False)
    manager = models.ForeignKey('auth.User', related_name='managed_areas', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
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
    user = models.ForeignKey('auth.User')
    project = models.ForeignKey(Project)
    joined_at = models.DateTimeField(auto_now_add=True)

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
    
    project = models.ForeignKey(Project, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_due = models.DateTimeField(null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    creator = models.ForeignKey('auth.User', related_name="created_tickets", editable=False)
    owners = models.ManyToManyField('auth.User', related_name="assigned_tickets", null=True, blank=True)
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='new')
    urgency = models.CharField(max_length=10, choices=TICKET_URGENCY_CHOICES, default='medium')
    type = models.CharField(max_length=11, choices=TICKET_TYPE_CHOICES, default='defect')

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

class Attachment(models.Model):
    ATTACHMENT_STATUS_CHOICES= (
        ('current', _('current')),
        ('superseded', _('superseded')),
        ('irrelevant', _('no longer relevant')),
    )
    
    creator = models.ForeignKey('auth.User')
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ATTACHMENT_STATUS_CHOICES, default='current')
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d')
    ticket = models.ForeignKey(Ticket, related_name="attachments")

    def __unicode__(self):
        return u'Attachment: %s' % self.attachment.name

def timeline_updater(sender, **kwargs):
    print kwargs
    instance = kwargs['instance']
    project = instance.project
    msg = _('Updated %(object)s') % {'object': sender.__name__}
    if kwargs.has_key('created') and kwargs['created']:
        msg = _('Created %(object)s') % {'object': sender.__name__}
    TimeLine.objects.create(project=project, description=msg, content_object=instance)

# Signals
signals.post_save.connect(timeline_updater, sender=Project)
signals.post_save.connect(timeline_updater, sender=Area)
signals.post_save.connect(timeline_updater, sender=Milestone)
signals.post_save.connect(timeline_updater, sender=Ticket)
