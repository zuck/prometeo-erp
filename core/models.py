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

from django.db import models
from django.db.models.signals import pre_delete
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Commentable(models.Model):
    """Template model for all commentable resources.
    """
    allow_comments = models.BooleanField(_('allow comments'), default=True)

    class Meta:
        abstract=True

@receiver(pre_delete)
def delete_comments(sender, **kwargs):
    """Deletes all associated comments.
    """
    comments = Comment.objects.for_model(sender)
    for c in comments:
        c.delete()
