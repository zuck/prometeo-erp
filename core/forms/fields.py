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

from time import localtime

from django.forms import fields
from django.utils import formats
from django.utils.translation import ugettext as _

from widgets import DateTimeWidget

class DateTimeField(fields.SplitDateTimeField):
    """A more-friendly date/time field.
    """
    widget = DateTimeWidget

    def compress(self, data_list):
        if data_list and data_list[0]:
            input_time = localtime()
            if len(data_list) > 1:
                input_time = data_list[1]
            datetime_string = "%s %s" % (data_list[0], input_time)
            return datetime_string
        return None
