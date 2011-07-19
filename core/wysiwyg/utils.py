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

import urllib
import os

from django.conf import settings

# Default max upload size: 1024 x 1024 x 10 = 10485760 bytes = 10 MB.
DEFAULT_FILE_MAX_UPLOAD_SIZE = 10485760

# Default upload root: 'MEDIA_ROOT/uploads'
DEFAULT_UPLOAD_ROOT = os.path.join(settings.MEDIA_ROOT, 'uploads')

# Default upload root: 'MEDIA_URL/uploads'
DEFAULT_UPLOAD_URL = os.path.join(settings.MEDIA_URL, 'uploads')

def get_max_upload_size():
    """Pull the FILE_UPLOAD_MAX_SIZE from settings.
    
    If the FILE_MAX_UPLOAD_SIZE is set to -1, no size limit is used.
    """
    return getattr(settings, 'FILE_UPLOAD_MAX_SIZE', DEFAULT_FILE_MAX_UPLOAD_SIZE)

def get_upload_root():
    """Pull the UPLOAD_ROOT variable from settings.
    """
    return getattr(settings, 'UPLOAD_ROOT', DEFAULT_UPLOAD_ROOT)

def get_upload_url():
    """Pull the UPLOAD_URL variable from settings.
    """
    return getattr(settings, 'UPLOAD_URL', DEFAULT_UPLOAD_URL)

def clean_path(url):
    """Makes the path safe from '.', '..', and multiple slashes.
    
    Ensure all slashes point the right direction '/'.
    """
    if not url:
        return '' 

    result = ''
    path = os.path.normpath(urllib.unquote(url))
    path = path.lstrip('/')
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        result = os.path.join(result, part).replace('\\', '/')
        
    if result and path != result or not path:
        result = ''
    
    return result
    
def strip_path(url):
    if not url:
        return '' 

    result = ''
    path = '/%s' % os.path.normpath(urllib.unquote(url))
    return path.replace(get_upload_url(), '').lstrip('/')

# Copied from python 2.6 
def commonprefix(m):
    """Given a list of pathnames, returns the longest common leading component.
    """
    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

# Copied from python 2.6 
def relpath(path, start=os.path.curdir):
    """Return a relative version of a path.
    """
    if not path:
        raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)
           
    # Work out how much of the filepath is shared by start and path.
    i = len(commonprefix([start_list, path_list]))
           
    rel_list = [os.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return os.path.join(*rel_list)

