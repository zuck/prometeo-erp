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

from hashlib import md5

from django import template

register = template.Library()

@register.simple_tag
def avatar(user, size=36, rating='g', default=None):
    """
    Returns an image element with gravatar for the specified user.

    Example tag usage: {% avatar user 80 "g" %}
    """
    
    # Verify the rating actually is a rating accepted by gravatar
    rating = rating.lower()
    ratings = ['g', 'pg', 'r', 'x']
    if rating not in ratings:
        raise template.TemplateSyntaxError('rating must be %s' % (", ".join(ratings)))
        
    # Create and return the url
    email = ""
    if user:
        email = user.email
    hash = md5(email).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s?s=%s&r=%s' % (hash, size, rating)
    if default:
        url = "%s&d=%s" % (url, default)
        
    return '<span class="avatar"><img width="%s" height="%s" src="%s" /></span>' % (size, size, url)

