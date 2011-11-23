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

from django.forms.fields import *
from django.forms.widgets import *
from django.forms.models import inlineformset_factory
from django.conf import settings

from prometeo.core.forms import enrich_form
from prometeo.core.forms.fields import *
from prometeo.core.forms.widgets import *

from models import *

class TaskForm(forms.ModelForm):
    """Form for Task data.
    """
    start = DateTimeField(required=False)
    end = DateTimeField(required=False)

    class Meta:
        model = Task
        exclude = ('user', 'closed')
        widgets = {
            'description': CKEditor(),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }

class TimesheetForm(forms.ModelForm):
    """Form for Timesheet data.
    """
    class Meta:
        model = Timesheet
        exclude = ('user',)
        widgets = {
            'date': DateWidget(),
        }

class TimesheetEntryForm(forms.ModelForm):
    """Form for TimesheetEntry data.
    """
    class Meta:
        model = TimesheetEntry
        widgets = {
            'start_time': TimeWidget(),
            'end_time': TimeWidget(),
        }

_TimesheetEntryFormset = inlineformset_factory(Timesheet, TimesheetEntry, form=TimesheetEntryForm, extra=2)

class TimesheetEntryFormset(_TimesheetEntryFormset):
    def __init__(self, *args, **kwargs):
        super(TimesheetEntryFormset, self).__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.forms[0].fields['start_time'].initial = settings.WORKING_DAY_START
            self.forms[0].fields['end_time'].initial = settings.LAUNCH_TIME_START
            self.forms[1].fields['start_time'].initial = settings.LAUNCH_TIME_END
            self.forms[1].fields['end_time'].initial = settings.WORKING_DAY_END
        elif len(self.forms) > 2:
            count = self.initial_form_count()+1
            self.forms = self.forms[:count]
            if count < self.total_form_count():
                self.forms[-1].fields['start_time'].required = False
                self.forms[-1].fields['end_time'].required = False
                self.forms[-1].fields['DELETE'].initial = True
            self.extra = 1

enrich_form(TaskForm)
enrich_form(TimesheetForm)
enrich_form(TimesheetEntryForm)
