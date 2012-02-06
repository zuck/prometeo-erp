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
from prometeo.partners.models import Job, Partner

from models import *

class JobForm(forms.ModelForm):
    """Form for Job data.
    """
    class Meta:
        model = Job
        widgets = {
            'contact': SelectAndAddWidget(add_url='/contacts/add'),
            'partner': SelectAndAddWidget(add_url='/partners/add'),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['partner'].queryset = Partner.objects.filter(is_managed=True)

class EmployeeForm(forms.ModelForm):
    """Form for Employee data.
    """
    class Meta:
        model = Employee
        exclude = ('job',)
        widgets = {
            'start': DateWidget(),
            'end': DateWidget(),
        }

class TimesheetForm(forms.ModelForm):
    """Form for Timesheet data.
    """
    class Meta:
        model = Timesheet
        widgets = {
            'date': DateWidget(),
            'employee': SelectAndAddWidget(add_url='/employees/add'),
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

class ExpenseVoucherForm(forms.ModelForm):
    """Form for ExpenseVoucher data.
    """
    class Meta:
        model = ExpenseVoucher
        widgets = {
            'date': DateWidget(),
            'employee': SelectAndAddWidget(add_url='contacts/add'),
        }

class ExpenseEntryForm(forms.ModelForm):
    """Form for ExpenseEntry data.
    """
    class Meta:
        model = ExpenseEntry
        widgets = {
            'date': DateWidget(),
        }

_ExpenseEntryFormset = inlineformset_factory(ExpenseVoucher, ExpenseEntry, form=ExpenseEntryForm, extra=5)

class ExpenseEntryFormset(_ExpenseEntryFormset):
    def __init__(self, *args, **kwargs):
        super(ExpenseEntryFormset, self).__init__(*args, **kwargs)
        count = self.initial_form_count()
        for i in range(0, self.total_form_count()-count):
            if i != 0 or count > 0:
                for field in self.forms[i+count].fields.values():
                    field.required = False
                self.forms[i+count].fields['DELETE'].initial = True

class LeaveRequestForm(forms.ModelForm):
    """Form for LeaveRequest data.
    """
    class Meta:
        model = LeaveRequest
        widgets = {
            'employee': SelectAndAddWidget(add_url='contacts/add'),
            'start': DateTimeWidget(),
            'end': DateTimeWidget(),
        }

enrich_form(JobForm)
enrich_form(EmployeeForm)
enrich_form(TimesheetForm)
enrich_form(TimesheetEntryForm)
enrich_form(ExpenseVoucherForm)
enrich_form(ExpenseEntryForm)
enrich_form(LeaveRequestForm)
