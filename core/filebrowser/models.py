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
import mimetypes
from datetime import datetime
from grp import getgrgid
from pwd import getpwuid

from django.conf import settings

from base import *

DEFAULT_PERMS = ['---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx']

class FileInfo(object):
    """Base object to store informations about files, folders and links.
    """
    def __init__(self, path):
        self._path = relative_to(path, settings.MEDIA_ROOT).strip('/')

    def __cmp__(self, other):
        if isinstance(other, FileInfo):
            if self.is_folder() and not other.is_folder():
                return -1
            elif not self.is_folder() and other.is_folder():
                return 1
            if self.abspath > other.abspath:
                return 1
            elif self.abspath == other.abspath:
                return 0
            elif self.abspath < other.abspath:
                return -1
        return 1

    def __repr__(self):
        return u'<FileInfo %s>' % self.abspath

    def _get_path(self):
        return self._path
    path = property(_get_path)

    def _get_abspath(self):
        return os.path.join(settings.MEDIA_ROOT, self.path)
    abspath = property(_get_abspath)

    def _get_name(self):
        return self.path.rpartition('/')[2]
    name = property(_get_name)

    def _get_ext(self):
        filepath, sep, ext = self.name.rpartition('.')
        if self.name != ext:
            return ext
        return None
    ext = property(_get_ext)

    def _get_copy_name(self):
        ext = self.ext
        if not ext:
            return '%s_copy' % self.name
        name = '%s_copy' % self.name[:-len(ext)].rstrip('.')
        return '.'.join([name, ext])
    copy_name = property(_get_copy_name)

    def _get_url(self):
        return path_to_url(self.abspath)
    url = property(_get_url)

    def _get_mimetype(self):
        return mimetypes.guess_type(self.abspath, False)[0]
    mimetype = property(_get_mimetype)

    def _get_perms(self):
        stats = self._stats()
        if stats:
            return "%04d" % int(oct(stats.st_mode & 0777))
        return None
    perms = property(_get_perms)

    def _get_user(self):
        stats = self._stats()
        if stats:
            return getpwuid(stats.st_uid)[0]
        return None
    user = property(_get_user)

    def _get_group(self):
        stats = self._stats()
        if stats:
            return getgrgid(stats.st_gid)[0]
        return None
    group = property(_get_group)

    def _get_created(self):
        stats = self._stats()
        if stats:
            return datetime.fromtimestamp(stats.st_ctime)
        return None
    created = property(_get_created)

    def _get_modified(self):
        stats = self._stats()
        if stats:
            return datetime.fromtimestamp(stats.st_mtime)
        return None
    modified = property(_get_modified)

    def _get_size(self):
        size = 0
        stats = self._stats()
        if stats:
            if self.is_folder():
                for dirpath, dirnames, filenames in os.walk(self.abspath):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            size += os.path.getsize(fp)
            else:
                size = stats.st_size
        return size
    size = property(_get_size)

    def _get_parent(self):
        if self.abspath.strip('/') != settings.MEDIA_ROOT.strip('/'):
            return FileInfo(get_parent(self.abspath))
        return None
    parent = property(_get_parent)

    def is_link(self):
        return os.path.islink(self.abspath)

    def is_broken_link(self):
        return self.is_link() and not self._stats()

    def is_folder(self):
        return os.path.isdir(self.abspath)

    def _stats(self):
        try:
            return os.stat(self.abspath)
        except OSError:
            return None
