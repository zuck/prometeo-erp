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

from django import forms as forms
from django.utils.translation import ugettext_lazy as _

from prometeo.core.forms import enrich_form
from prometeo.core.forms.fields import *
from prometeo.core.forms.widgets import *

from models import *

class ImportEventsForm(forms.Form):
    """Form to input an .ics file.
    """
    file  = forms.FileField(label=_("Select an .ics file"))

class EventForm(forms.ModelForm):
    """Form for event data.
    """
    start = SplitDateTimeField()
    end = SplitDateTimeField(required=False)

    class Meta:
        model = Event
        exclude = ('author', 'stream')
        widgets = {
            'description': CKEditor(),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }

enrich_form(EventForm)
