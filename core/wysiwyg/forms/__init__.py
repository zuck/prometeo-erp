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

import os 

from django import forms
from django.utils.translation import ugettext as _

from .. import utils

class DirectoryFileForm(forms.Form):

    link = forms.ChoiceField(help_text=_('Link Destination'))

    def __init__(self, file, *args, **kwargs):
        self.file = file 
        self.upload_root = utils.get_upload_root()
        super(DirectoryFileForm, self).__init__(*args, **kwargs)
    
        # Set the choices dynamicly.
        self.fields['link'].choices = self.make_choices()

    def make_choices(self):
 
        choices = []

        # Make "/" valid"
        d = self.upload_root
        d_short = d.replace(self.upload_root, "", 1)
        if not d_short:
            d_short = '/'
        
        choices.append((d, d_short))

        for root, dirs, files in os.walk(self.upload_root):
            for d in dirs:
                d = os.path.join(root, d)
                d_short = d.replace(self.upload_root, "", 1)
                choices.append((d, d_short))
            for f in files:
                f = os.path.join(root, f)
                f_short = f.replace(self.upload_root, "", 1)
                choices.append((f, f_short))


        #return sorted(choices)      
        choices.sort()
        return choices

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)

        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))
            if path.startswith(self.original):
                raise forms.ValidationError(_('Can\'t move directory into itself.'))

        if not os.access(parent, os.W_OK):
            raise forms.ValidationError(_('Can not write to directory.'))

        return parent

class DirectoryForm(forms.Form):

    parent = forms.ChoiceField(help_text=_('Destination Directory'))

    def __init__(self, file, original, *args, **kwargs):
        self.file = file 
        self.original = original 
        self.upload_root = utils.get_upload_root()
        super(DirectoryForm, self).__init__(*args, **kwargs)
    
        # Set the choices dynamicly.
        self.fields['parent'].choices = self.make_choices()

    def make_choices(self):
 
        choices = []

        # Make "/" valid"
        d = self.upload_root
        d_short = d.replace(self.upload_root, "", 1)
        if not d_short:
            d_short = '/'
        
        choices.append((d, d_short))

        for root, dirs, files in os.walk(self.upload_root):
            for d in dirs:
                d = os.path.join(root, d)
                if not d.startswith(self.original): 
                    d_short = d.replace(self.upload_root, "", 1)
                    choices.append((d, d_short))

        #return sorted(choices)      
        choices.sort()
        return choices

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)

        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))
            if path.startswith(self.original):
                raise forms.ValidationError(_('Can\'t move directory into itself.'))

        if not os.access(parent, os.W_OK):
            raise forms.ValidationError(_('Can not write to directory.'))

        return parent

class NameForm(forms.Form):

    def __init__(self, path, original, *args, **kwargs):
        self.path = path
        self.original = original
        super(NameForm, self).__init__(*args, **kwargs)

    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name']
        
        path = os.path.join(self.path, name)

        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Name already exists.'))

        return name

class CopyForm(NameForm,DirectoryForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        name = self.cleaned_data.get('name')
        parent = self.cleaned_data.get('parent')
        
        path = os.path.join(parent, name)

        if os.access(path, os.F_OK):
            raise forms.ValidationError(_('File name already exists.'))

        return cleaned_data

class CreateLinkForm(NameForm,DirectoryFileForm):
    pass

class UploadForm(forms.Form):

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(UploadForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=False)  
    file = forms.FileField()

    def clean_file(self):
        filename = self.cleaned_data['name'] or self.cleaned_data['file'].name

        if os.access(os.path.join(self.path, filename), os.F_OK):
            raise forms.ValidationError(_('File already exists.')) 
        
        # CHECK FILESIZE
        max_filesize = utils.get_max_upload_size()
        filesize = self.cleaned_data['file'].size
        if max_filesize != -1 and filesize > max_filesize:
            raise forms.ValidationError(_(u'Filesize exceeds allowed Upload Size.'))

        return self.cleaned_data['file']
