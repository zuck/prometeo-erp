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
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

ckeditor_path = getattr(settings, 'CKEDITOR_PATH', 'js/ckeditor/')

class CKEditor(forms.Textarea):

    class Media:
        js = (ckeditor_path + 'ckeditor.js',)

    def render(self, name, value, attrs={}):
        rendered = super(CKEditor, self).render(name, value, attrs)
        tokens = {
            'name': name,
            'browse_url': reverse('admin_wysiwyg_index'),
            'image_browse_url': reverse('admin_wysiwyg_index'),
            'upload_url': reverse('admin_wysiwyg_upload', args=[None]),
            'image_upload_url': reverse('admin_wysiwyg_upload', args=[None]),
        }
        rendered += mark_safe(u'<script type="text/javascript">'                                                \
                              u'   CKEDITOR.replace("%(name)s",'                                                \
                              u'       {'                                                                       \
                              u'           skin: "v2",'                                                         \
                              u'           toolbar: "Full",'                                                    \
                              u'           height: "220",'                                                      \
                              u'           width: "785",'                                                       \
                              u'           filebrowserBrowseUrl: "%(browse_url)s",'                             \
					          u'           filebrowserImageBrowseUrl: "%(image_browse_url)s",'                  \
					          u'           filebrowserUploadUrl: "%(upload_url)s",'                             \
					          u'           filebrowserImageUploadUrl: "%(image_upload_url)s",'                  \
                              u'       }'                                                                       \
                              u'   );'                                                                          \
                              u'</script>' % tokens)
        return rendered
