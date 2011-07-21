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

from django import forms
from django.contrib.formtools import wizard
from django.views.generic.simple import redirect_to
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from prometeo.core.wysiwyg.forms.widgets import CKEditor

from models import *

class ProjectForm(forms.ModelForm):
    """Form for project data.
    """
    class Meta:
        model = Project
        exclude = ('id', 'closed')
        widgets = {
            'description': CKEditor(),
            'tease': CKEditor(),
        }

class MilestoneForm(forms.ModelForm):
    """Form for milestone data.
    """
    class Meta:
        model = Milestone
        
class TicketForm(forms.ModelForm):
    """Form for ticket data.
    """
    class Meta:
        model = Ticket
        exclude = ('project', 'milestone', 'areas', 'author', 'assignees', 'closed', 'public', 'allow_comments')
        widgets = {'description': CKEditor(),}
        
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        if self.instance is None or self.instance.pk is None:
            del self.fields['status']
