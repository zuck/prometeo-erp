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

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from models import *

@login_required
def stream_follow(request, slug, path='/', **kwargs):
    """Registers the current user to the given stream.
    """
    stream = get_object_or_404(Stream, slug=slug)

    if request.user not in stream.followers.all():
        stream.followers.add(request.user)

    messages.success(request, _("You're now following the stream."))

    return redirect_to(request, permanent=False, url=path)

@login_required
def stream_leave(request, slug, path='/', **kwargs):
    """Un-registers the current user from the given stream.
    """
    stream = get_object_or_404(Stream, slug=slug)

    if request.user in stream.followers.all():
        stream.followers.remove(request.user)

    messages.success(request, _("You don't follow this stream anymore."))

    return redirect_to(request, permanent=False, url=path)

    
