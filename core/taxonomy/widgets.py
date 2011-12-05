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

import random

from models import Category, Tag

def categories(context):
    """Returns the category hierarchy.
    """
    context['categories'] = Category.objects.filter(parent=None).select_related()
    return context
    
def tag_cloud(context):
    """Returns the cloud of most 15 used tags.
    """
    context['tag_max_occurences'] = 0
    tags = Tag.objects.all()
    valid_tags = sorted([t for t in tags if len(t.occurences) > 0], key=lambda t: len(t.occurences))[:15]
    if valid_tags:
        context['tag_max_occurences'] = len(valid_tags[-1].occurences)
    final_tags = []
    while (len(valid_tags) > 0):
        index = int(random.random()*len(valid_tags))
        final_tags.append(valid_tags.pop(index))
    context['tags'] = final_tags
    return context
