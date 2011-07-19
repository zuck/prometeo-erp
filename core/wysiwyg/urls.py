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

# Admin views.
urlpatterns = patterns('prometeo.core.wysiwyg.views',

    # Common operations.
    url(r'^delete/(?P<url>.*)$', 'admin_delete', name='admin_wysiwyg_delete'),

    url(r'^copy/(?P<url>.*)$', 'admin_copy', name='admin_wysiwyg_copy'),

    url(r'^move/(?P<url>.*)$', 'admin_move', name='admin_wysiwyg_move'),

    url(r'^rename/(?P<url>.*)$', 'admin_rename', name='admin_wysiwyg_rename'),
  
    # File Operations.
    url(r'^upload/(?P<url>.*)$', 'admin_upload', name='admin_wysiwyg_upload'),
    
    url(r'^select/(?P<url>.*)$', 'admin_select', name='admin_wysiwyg_select'),

    # Link Options.
    url(r'^mkln/(?P<url>.*)$', 'admin_mkln', name='admin_wysiwyg_mkln'),

    # Directory Options.
    url(r'^mkdir/(?P<url>.*)$', 'admin_mkdir', name='admin_wysiwyg_mkdir'),

    url(r'^browse/(?P<url>.*)$', 'admin_index', name='admin_wysiwyg_list'),

    url(r'^browse/$', 'admin_index', name='admin_wysiwyg_index'),
)

urlpatterns += patterns('django.views.generic.simple',

    url(r'^$', 'redirect_to', {'url': 'browse/'}),
)
