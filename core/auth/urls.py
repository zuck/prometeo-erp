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

from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url(r'^users/$', view='prometeo.core.auth.views.user_list', name='user_list'),
    url(r'^users/login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='user_login'),
    url(r'^users/logged/$', 'prometeo.core.auth.views.user_logged'),
    url(r'^users/logout/$', view='django.contrib.auth.views.logout_then_login', name='user_logout'),
    url(r'^users/add/$', view='prometeo.core.auth.views.user_add', name='user_add'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/$', view='prometeo.core.auth.views.user_detail', name='user_detail'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/edit/$', view='prometeo.core.auth.views.user_edit', name='user_edit'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/delete/$', view='prometeo.core.auth.views.user_delete', name='user_delete'),

    url(r'^comments/(?P<id>\d+)/delete/$', view='prometeo.core.auth.views.comment_delete', name='comment_delete'),
)
