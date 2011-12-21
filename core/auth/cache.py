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

# Inspired by http://stackoverflow.com/a/7469395/1063729

class _Singleton(type):
    """Singleton pattern.
    """
    def __init__(cls, name, bases, dicts):
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls.instance

class LoggedInUserCache(object):
    """Stores the current user as a member attribute of a singleton.
    """
    __metaclass__ = _Singleton

    user = None

    def set_user(self, request):
        if request.user.is_authenticated():
            self.user = request.user

    @property
    def current_user(self):
        return self.user

    @property
    def has_user(self):
        return user is not None
