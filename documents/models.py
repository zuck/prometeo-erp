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

import os
from datetime import date

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from prometeo.core.models import Commentable

def _get_upload_to(instance, filename):
    today = date.today()
    return os.path.join('documents', '%d' % instance.document.owner.pk, '%s' % today.year, '%s' % today.month, filename)

class Document(Commentable):
    """Document model.
    """
    code = models.CharField(max_length=255, verbose_name=_('code'))
    owner = models.ForeignKey('partners.Partner', verbose_name=_('owner'))
    status = models.CharField(max_length=20, choices=settings.DOCUMENT_STATUS_CHOICES, default=settings.DOCUMENT_DEFAULT_STATUS, verbose_name=_('status'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey('auth.User', verbose_name=_('created by'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    categories = models.ManyToManyField('taxonomy.Category', null=True, blank=True, verbose_name=_('categories'))
    tags = models.ManyToManyField('taxonomy.Tag', null=True, blank=True, verbose_name=_('tags'))
    stream = models.OneToOneField('streams.Stream', null=True, verbose_name=_('stream'))

    class Meta:
        ordering = ('owner', '-created')
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        
    def __unicode__(self):
        return "#%s: %s" % (self.code, self.content_object)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()
    
    def get_edit_url(self):
        return self.content_object.get_edit_url()
    
    def get_delete_url(self):
        return self.content_object.get_delete_url()

class HardCopy(models.Model):
    """A localized hard copy of a document.
    """
    document = models.ForeignKey(Document, verbose_name=_('document'))
    file = models.FileField(upload_to=_get_upload_to, null=True, blank=True, verbose_name=_('file'))
    language = models.CharField(max_length=5, null=True, blank=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))

    class Meta:
        ordering = ('document', 'language')
        verbose_name = _('hard copy')
        verbose_name_plural = _('hard copies')
        
    def __unicode__(self):
        return "%s | %s" % (self.document, self.language)
