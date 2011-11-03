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
import shutil

import django.dispatch
from django.db import models
from django.conf import settings

## UTILS ##

def manage_files(cls):
    """Connects handlers for files management.
    """
    models.signals.post_save.connect(create_files_root, cls)
    models.signals.pre_delete.connect(delete_files_root, cls)

## HANDLERS ##

def create_files_root(sender, instance, *args, **kwargs):
    """Creates the root which contains all the files associated with this object.
    """
    if 'created' in kwargs:
        root_path = instance.get_files_root()
        if not os.access(root_path, os.F_OK):
            os.makedirs(root_path)

def delete_files_root(sender, instance, *args, **kwargs):
    """Deletes the root which contains all the files associated with this object.
    """
    root_path = instance.get_files_root()
    if os.access(root_path, os.F_OK):
        shutil.rmtree(root_path)
