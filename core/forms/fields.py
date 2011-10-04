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

from time import strptime, strftime, localtime

from django import forms
from django.db import models
from django.forms.fields import *
from django.utils.translation import ugettext as _

from widgets import SplitDateTimeWidget

class SplitDateTimeField(MultiValueField):
    """A more-friendly date/time field.

    Inspired by:

    http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/
    """
    widget = SplitDateTimeWidget

    def __init__(self, *args, **kwargs):
        fields = (
            CharField(max_length=10),
            CharField(max_length=2),
            CharField(max_length=2),
            ChoiceField(choices=[('AM','AM'),('PM','PM')])
        )
        super(SplitDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list and data_list[0]:
            if data_list[1] and data_list[2] and data_list[3]:
                input_time = strptime("%s:%s %s" % (data_list[1], data_list[2], data_list[3]), "%I:%M %p")
            else:
                input_time = localtime()
            datetime_string = "%s %s" % (data_list[0], strftime('%H:%M', input_time))
            return datetime_string
        return None
