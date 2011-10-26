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

from django.conf.urls.defaults import *

from base import *

urlpatterns = patterns('prometeo.core.filebrowser.views',

    url(r'^mkdir/(?P<url>.*)$', 'mkdir', name='file_mkdir'),
    url(r'^upload/(?P<url>.*)$', 'upload', name='file_upload'),
    url(r'^move/(?P<url>.*)$', 'move', name='file_move'),
    url(r'^copy/(?P<url>.*)$', 'copy', name='file_copy'),
    url(r'^mkln/(?P<url>.*)$', 'mkln', name='file_mkln'),
    url(r'^rename/(?P<url>.*)$', 'rename', name='file_rename'),
    url(r'^delete/(?P<url>.*)$', 'delete', name='file_delete'),
    url(r'^%s/(?P<url>.*)$' % MEDIA_BASE_URL, 'browse', name='file_browse'),
)
