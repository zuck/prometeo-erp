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

from base import DEBUG, TEMPLATE_CONTEXT_PROCESSORS, MIDDLEWARE_CLASSES

AUTH_PROFILE_MODULE = 'auth.UserProfile'
AUTH_EXPIRATION_DAYS = 2

LOGIN_URL = '/users/login'
LOGOUT_URL = '/users/logout'
LOGIN_REDIRECT_URL = '/users/logged/'

LOGIN_REQUIRED_URLS = (
    r'/(.*)$',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/static/(.*)$',
    r'/users/login/$',
    r'/users/register/$',
    r'/users/activate/(.*)$',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'prometeo.core.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES += (
    'prometeo.core.auth.middleware.RequireLoginMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'prometeo.core.auth.backends.ObjectPermissionBackend',
)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
