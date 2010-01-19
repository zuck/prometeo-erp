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

import os
from django.conf.urls.defaults import *
from django.conf import settings

if not hasattr(settings, 'TEMPLATE_DIRS'):
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

def get_url_patterns():
    """Return URL patterns of all installed apps after 'prometeo.core'.
    """
    urlpatterns = patterns("", (r'^', include('prometeo.core.urls')))
    i = settings.INSTALLED_APPS.index('prometeo.core')
    for module in settings.INSTALLED_APPS[i+1:]:
        if not module.startswith('django'):
            (pkg, sep, name) = module.rpartition('.')
            urlpatterns += patterns("", (r'^%s/' % name, include('%s.urls' % module)))

    return urlpatterns
