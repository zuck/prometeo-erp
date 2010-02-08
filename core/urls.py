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

__author__ = 'Emanuele Bertoldi <zuck@fastwebnet.it>'
__copyright__ = 'Copyright (c) 2010 Emanuele Bertoldi'
__version__ = '$Revision$'

from django.conf.urls.defaults import *
from django.conf import settings
import imp

urlpatterns = patterns('',

    # Start page.
    (r'^$', 'core.views.start'),
    
    # Media files.
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    
    # Comments framework.
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # Accounts.
    (r'^accounts/$', 'core.views.index'),
    (r'^accounts/add/$', 'core.views.add'),
    (r'^accounts/view/(?P<id>\d+)/$', 'core.views.view'),
    (r'^accounts/edit/(?P<id>\d+)/$', 'core.views.edit'),
    (r'^accounts/delete/(?P<id>\d+)/$', 'core.views.delete'),
    (r'^accounts/logged/$', 'core.views.logged'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login')
)

def autodiscover():
    """ Auto discover urls of installed applications.
    """    
    for app in settings.INSTALLED_APPS:
        if app.startswith('django'):
            continue
            
        # Step 1: find out the app's __path__.
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's urls.py.
        try:
            imp.find_module('urls', app_path)
        except ImportError:
            continue

        # Step 3: return the app's url patterns.
        pkg, sep, name = app.rpartition('.')
        global urlpatterns
        urlpatterns += patterns("", (r'^%s/' % name, include('%s.urls' % app)))
