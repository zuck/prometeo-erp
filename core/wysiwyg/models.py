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

from django.db import models

class Items(models.Model):
    class Meta:
        db_table = None
        permissions = (
            ("can_copy_file", "Can copy file"),
            ("can_upload_file", "Can upload file"),
            ("can_delete_file", "Can delete file"),
            ("can_rename_file", "Can rename file"),
            ("can_move_file", "Can move file"),

            ('can_create_symlink', 'Can create symlink'),
            ('can_copy_symlink', 'Can copy symlink'),
            ('can_move_symlink', 'Can move symlink'),
            ('can_rename_symlink', 'Can rename symlink'),
            ('can_delete_symlink', 'Can delete symlink'),

            ("can_copy_dir", "Can copy directory"),
            ("can_delete_dir", "Can delete directory"),
            ("can_rename_dir", "Can rename directory"),
            ("can_create_dir", "Can make directory"),
            ("can_move_dir", "Can move directory"),
        )
