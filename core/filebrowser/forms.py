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

import os 

from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from prometeo.core.forms import enrich_form

from base import *

def _make_dest_choices(path, *args, **kwargs):
    """Generates the list of directories in the root's subtree.
    """
    choices = []
    root_path = kwargs.get('root', None) or settings.MEDIA_ROOT or '/'
    
    choices.append((root_path, path_to_url(root_path)))

    for root, dirs, files in os.walk(root_path):
        for d in dirs:
            d = os.path.join(root, d)
            if d != path:
                choices.append((d, path_to_url(d)))
 
    choices.sort()

    return choices

class NameForm(forms.Form):
    """Form to select a name for a file, folder or link.
    """
    name = forms.CharField()

    def __init__(self, path, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        self.path = path

    def clean_name(self):
        name = self.cleaned_data['name']

        if name and os.access(os.path.join(self.path, name), os.F_OK):
            raise forms.ValidationError(_('The name already exists.'))

        return name

class DestinationForm(forms.Form):
    """Form to select a destination for a file, folder or link.
    """
    destination = forms.ChoiceField()

    def __init__(self, path, *args, **kwargs):
        super(DestinationForm, self).__init__(*args, **kwargs)
        self.fields['destination'].choices = _make_dest_choices(path, *args, **kwargs)
        self.source_path = path

    def clean_destination(self):
        destination = self.cleaned_data['destination']

        if destination != get_parent(self.source_path):
            if not os.access(destination, os.W_OK):
                raise forms.ValidationError(_('Can not write to this folder.'))

            name = get_name(self.source_path)

            if name and os.access(os.path.join(destination, name), os.F_OK):
                raise forms.ValidationError(_('The name already exists in this folder.'))

        return destination

class NameDestinationForm(forms.Form):
    """Form to select destination and name for a file, folder or link.
    """
    name = forms.CharField(required=False)
    destination = forms.ChoiceField()

    def __init__(self, path, *args, **kwargs):
        super(NameDestinationForm, self).__init__(*args, **kwargs)
        self.fields['destination'].choices = _make_dest_choices(path, *args, **kwargs)
        self.source_path = path

    def clean_destination(self):
        destination = self.cleaned_data['destination']

        if destination != get_parent(self.source_path):
            if not os.access(destination, os.W_OK):
                raise forms.ValidationError(_('Can not write to the given folder.'))

            name = self.cleaned_data.get('name', None) or get_name(self.source_path)

            if name and os.access(os.path.join(destination, name), os.F_OK):
                raise forms.ValidationError(_('The name already exists.'))

        return destination

class UploadForm(forms.Form):
    """Form to upload a new file.
    """
    name = forms.CharField(required=False)
    file = forms.FileField()

    def __init__(self, path, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.path = path

    def clean_file(self):
        name = self.cleaned_data.get('name', None) or self.cleaned_data['file'].name
        path = os.path.join(self.path, name)

        if os.access(path, os.F_OK):
            raise forms.ValidationError(_('The name already exists.')) 

        max_filesize = get_max_upload_size()
        filesize = self.cleaned_data['file'].size
        if max_filesize != -1 and filesize > max_filesize:
            raise forms.ValidationError(_('The file exceeds the allowed upload size.'))

        return self.cleaned_data['file']

enrich_form(NameForm)
enrich_form(DestinationForm)
enrich_form(NameDestinationForm)
enrich_form(UploadForm)
