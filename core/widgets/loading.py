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

import types

from django.conf import settings

class WidgetCache(object):
    def __init__(self):
        self.__discovered = False
        self.__sources = []

    def __get_sources(self):
        self.__discover_widgets()
        return self.__sources
    sources = property(__get_sources)

    def __discover_widgets(self):
        if self.__discovered:
            return
        for app in settings.INSTALLED_APPS:
            if app.startswith('django'):
                continue
            try:
                module_name = "%s.widgets" % app
                module = __import__(module_name, {}, {}, ['*'])
                for a in dir(module):
                    if isinstance(module.__dict__.get(a), types.FunctionType):
                        source = "%s.%s" % (module_name, a)
                        self.__sources.append((source, source))
            except ImportError:
                pass
        self.__discovered = True

registry = WidgetCache()

