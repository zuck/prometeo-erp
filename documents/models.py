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
from django.core.urlresolvers import reverse
from django.conf import settings

from prometeo.core.models import Commentable

from managers import *

def _get_upload_to(instance, filename):
    return os.path.join(
        'documents',
        '%d' % instance.document.owner.pk,
        u'%s' % instance.document.content_type,
        u'%s' % instance.document.created.year,
        u'%s' % instance.document.created.month,
        filename
    )

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

    objects = DocumentManager()

    class Meta:
        ordering = ('owner', '-created')
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        if self.content_type and not self.code:
            year = date.today().year
            uid = 1
            try:
                last_doc = Document.objects.filter(content_type=self.content_type, code__endswith='-%s' % year).latest('created')
                uid = int(last_doc.code.partition('-')[0]) + 1
            except:
                pass
            self.code = '%d-%s' % (uid, year)

    def __unicode__(self):
        return "%s #%s" % (self.content_object, self.code)

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
    file = models.FileField(upload_to=_get_upload_to, verbose_name=_('file'))
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))

    class Meta:
        ordering = ('document', 'language')
        verbose_name = _('hard copy')
        verbose_name_plural = _('hard copies')
        
    def __unicode__(self):
        return "%s | %s" % (self.document, self.language)

    def get_absolute_url(self):
        return self.file.url

    def get_delete_url(self):
        return reverse('file_delete', args=[self.get_absolute_url().lstrip('/')])
