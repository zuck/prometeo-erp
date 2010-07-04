#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

from django.utils.translation import ugettext_lazy as _
from django import forms

from models import *

class ProjectForm(forms.ModelForm):
    """Form for project data.
    """
    class Meta:
        model = Project
        exclude = ('members', 'date_closed')
        
class AreaForm(forms.ModelForm):
    """Form for area data.
    """
    class Meta:
        model = Area
        exclude = ('project',)

class MilestoneForm(forms.ModelForm):
    """Form for milestone data.
    """
    class Meta:
        model = Milestone
        exclude = ('project', 'date_completed',)
        
    def clean_date_due(self):
        ddate = self.cleaned_data['date_due']
        parent = self.cleaned_data['parent']
        if parent and parent.date_due and ddate > parent.date_due:
            raise forms.ValidationError(_("The date due is greater than the parent's one."))
        return ddate
        
class TicketForm(forms.ModelForm):
    """Form for ticket data.
    """
    class Meta:
        model = Ticket
        exclude = ('project', 'date_closed',)
        
class AreaTicketForm(forms.ModelForm):
    """Form for area ticket data.
    """
    class Meta:
        model = Ticket
        exclude = ('project', 'area', 'date_closed',)
        
class MilestoneTicketForm(forms.ModelForm):
    """Form for milestone ticket data.
    """
    class Meta:
        model = Ticket
        exclude = ('project', 'milestone', 'date_closed',)
        
class MembershipForm(forms.ModelForm):
    """Form for membership data.
    """
    class Meta:
        model = Membership
        exclude = ('project')
