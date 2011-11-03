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

import urllib
import os

from django.conf import settings

# Default max upload size: 1024 x 1024 x 10 = 10485760 bytes = 10 MB.
DEFAULT_FILE_MAX_UPLOAD_SIZE = 10485760

def get_max_upload_size():
    """Pull the FILE_UPLOAD_MAX_SIZE from settings.
    
    If the FILE_MAX_UPLOAD_SIZE is set to -1, no size limit is used.
    """
    return getattr(settings, 'FILE_UPLOAD_MAX_SIZE', DEFAULT_FILE_MAX_UPLOAD_SIZE)
    
def relative_to(uri, rel):
    """Returns only the relative URI from "rel".
    """
    return os.path.normpath(uri).replace(os.path.normpath(rel), '')

def get_parent(uri):
    """Returns the path to the parent URI.
    """
    return os.path.normpath(uri).rpartition('/')[0]

def get_name(uri):
    """Returns the name of the given URI.
    """
    return os.path.normpath(uri).rpartition('/')[2]

def url_to_path(url, root_path=settings.MEDIA_ROOT, root_url=settings.MEDIA_URL):
    """Converts a valid URL into the relative server-side path.
    """
    return os.path.join(root_path, relative_to(url, root_url).lstrip('/'))

def path_to_url(path, root_path=settings.MEDIA_ROOT, root_url=settings.MEDIA_URL):
    """Converts a valid server-side path into the relative URL.
    """
    return os.path.join(root_url, relative_to(path, root_path).lstrip('/'))
