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

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from prometeo.core.forms import enrich_form
from prometeo.core.forms.fields import *
from prometeo.core.forms.widgets import *

from models import *

class WikiPageForm(forms.ModelForm):
    """Form for wiki page data.
    """
    class Meta:
        model = WikiPage
        exclude = ('author', 'stream')
        widgets = {
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

class FaqForm(forms.ModelForm):
    """Form for FAQ data.
    """
    class Meta:
        model = Faq
        exclude = ['author', 'created', 'stream']
        widgets = {
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

class AnswerForm(forms.ModelForm):
    """Form for answer data.
    """
    class Meta:
        model = Answer
        exclude = ['question', 'author', 'created', 'allow_comments']

class PollForm(forms.ModelForm):
    """Form for poll data.
    """
    class Meta:
        model = Poll
        exclude = ['author', 'created', 'stream']
        widgets = {
            'due_date': DateWidget(),
            'categories': SelectMultipleAndAddWidget(add_url='/categories/add', with_perms=['taxonomy.add_category']),
            'tags': SelectMultipleAndAddWidget(add_url='/tags/add', with_perms=['taxonomy.add_tag'])
        }

class ChoiceForm(forms.ModelForm):
    """Form for choice data.
    """
    class Meta:
        models = Choice
        exclude = ['poll',]

_ChoiceFormset = inlineformset_factory(Poll, Choice, form=ChoiceForm, extra=4)

class ChoiceFormset(_ChoiceFormset):
    def __init__(self, *args, **kwargs):
        super(ChoiceFormset, self).__init__(*args, **kwargs)
        count = self.initial_form_count()
        for i in range(0, self.total_form_count()-count):
            if i > 1 or count > 0:
                for field in self.forms[i+count].fields.values():
                    field.required = False
                self.forms[i+count].fields['DELETE'].initial = True

enrich_form(WikiPageForm)
enrich_form(FaqForm)
enrich_form(PollForm)
enrich_form(ChoiceForm)
