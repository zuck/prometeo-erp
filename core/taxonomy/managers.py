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

from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

class VoteManager(models.Manager):
    """Custom manager for Vote model.
    """
    def get_for_model(self, m):
        ctype = ContentType.objects.get_for_model(m)
        if isinstance(m, models.Model):
            return self.filter(content_type=ctype, object_id=m.pk)
        return self.filter(content_type=ctype)

    def get_for_models(self, ms):
        qs = Q()
        for m in ms:
            ctype = ContentType.objects.get_for_model(m)
            if isinstance(m, models.Model):
                qs |= Q(content_type=ctype, object_id=m.pk)
            else:
                qs |= Q(content_type=ctype)
        return self.filter(qs)
