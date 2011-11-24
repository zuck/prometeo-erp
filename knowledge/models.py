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

import datetime

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

from prometeo.core.utils import value_to_string
from prometeo.core.models import Commentable

from managers import *

class WikiPage(Commentable):
    """Wiki page model.
    """
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(help_text=_('Use MarkDown syntax.'), verbose_name=_('body'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    author = models.ForeignKey('auth.User', verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('wiki page')
        verbose_name_plural = _('wiki pages')     

    def __unicode__(self):
        return u'%s' % self.slug

    @models.permalink
    def get_absolute_url(self):
        return ("wikipage_detail", (), {"slug": self.slug})

    @models.permalink
    def get_edit_url(self):
        return ("wikipage_edit", (), {"slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        return ("wikipage_delete", (), {"slug": self.slug})
        
class WikiRevision(models.Model):
    """Revision of a wiki page.
    """
    page = models.ForeignKey(WikiPage, related_name='revisions', verbose_name=_('page'))
    slug = models.SlugField(verbose_name=_('slug'))
    body = models.TextField(verbose_name=_('body'))
    author = models.ForeignKey(User, verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))

    objects = WikiRevisionManager()

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('wiki page revision')
        verbose_name_plural = _('wiki page revisions')     

    def __unicode__(self):
        return _(u'Rev # %(created)s') % {'created': value_to_string(self.created)}

    @models.permalink
    def get_absolute_url(self):
        return ("wikipage_revision_detail", (), {"slug": self.page.slug, "created": self.created})

class Faq(Commentable):
    """Frequently Asked Question model.
    """
    title = models.CharField(max_length=200, unique=True, verbose_name=_('title'))
    question = models.TextField(verbose_name=_('question'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    best_answer = models.ForeignKey('comments.Comment', null=True, blank=True, verbose_name=_('best answer'))
    author = models.ForeignKey('auth.User', verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

    @models.permalink
    def get_absolute_url(self):
        return ("faq_detail", (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ("faq_edit", (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ("faq_delete", (), {"id": self.pk})

    def __unicode__(self):
        return u'%s' % self.title

class Poll(Commentable):
    """Poll model.
    """    
    title = models.CharField(unique=True, max_length=100, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_('language'))
    author = models.ForeignKey(User, verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    due_date = models.DateTimeField(null=True, blank=True, verbose_name=_('due date'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))

    class Meta:
        ordering  = ('-created',)
        get_latest_by = 'created'
        verbose_name = _('poll')
        verbose_name_plural = _('polls')

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ("poll_detail", (), {"id": self.pk})

    @models.permalink
    def get_edit_url(self):
        return ("poll_edit", (), {"id": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ("poll_delete", (), {"id": self.pk})

    def _vote_count(self):
        count = 0
        for choice in self.choices.all():
            count += choice.votes.count()
        return count
    _vote_count.short_description = _('vote count')
    vote_count = property(_vote_count)
   
class Choice(models.Model):
    """Choice model.
    """    
    poll = models.ForeignKey(Poll, related_name='choices', verbose_name=_('poll'))
    description = models.CharField(max_length=255, verbose_name=_('description'))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_('sort order'))

    class Meta:
        ordering  = ('poll', 'sort_order',)
        verbose_name = _('choice')
        verbose_name_plural = _('choices')

    @models.permalink
    def get_absolute_url(self):
        return ("poll_vote", (), {"id": self.poll.pk, "choice": self.sort_order})

    def __unicode__(self):
        return u'%s' % self.description
        
class Vote(models.Model):
    """Vote model.
    """    
    choice = models.ForeignKey(Choice, related_name='votes', verbose_name=_('choice'))
    owner = models.ForeignKey(User, related_name='poll_votes', verbose_name=_('owner'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
