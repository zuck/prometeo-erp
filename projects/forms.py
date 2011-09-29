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

from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _

from prometeo.core import forms
from prometeo.core.wysiwyg.forms.widgets import CKEditor

from models import *

class ProjectForm(forms.ModelForm):
    """Form for project data.
    """
    class Meta:
        model = Project
        exclude = ('author', 'slug', 'closed', 'dashboard', 'stream')
        widgets = {
            'description': CKEditor(),
            'tags': forms.SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': forms.SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }

class MilestoneForm(forms.ModelForm):
    """Form for milestone data.
    """
    class Meta:
        model = Milestone
        exclude = ('project', 'slug', 'author', 'closed', 'dashboard', 'stream')
        widgets = {
            'description': CKEditor(),
            'tags': forms.SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': forms.SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }
        
    def clean_date_due(self):
        ddate = self.cleaned_data['date_due']
        if ddate:
            parent = self.cleaned_data['parent']
            if parent and parent.date_due and ddate > parent.date_due:
                raise django_forms.ValidationError(_("The date due is greater than the parent's one."))
        return ddate
        
class TicketForm(forms.ModelForm):
    """Form for ticket data.
    """
    class Meta:
        model = Ticket
        exclude = ('project', 'author', 'closed', 'public', 'allow_comments', 'stream')
        widgets = {
            'tags': forms.SelectMultipleAndAddWidget(add_url='/tags/add/'),
            'categories': forms.SelectMultipleAndAddWidget(add_url='/categories/add/'),
        }
        
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        if self.instance is None or self.instance.pk is None:
            del self.fields['status']
        self.fields['milestone'].queryset = self.instance.project.milestone_set.all()
