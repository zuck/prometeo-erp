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

from django.contrib import admin
from prometeo.core.wysiwyg.forms.widgets import CKEditor

from models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'created', 'status')
    list_filter   = ('created', 'closed', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    formfield_overrides = { models.TextField: {'widget' : CKEditor} }

class AreaAdmin(admin.ModelAdmin):
    list_display  = ('title',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = { models.TextField: {'widget' : CKEditor} }

class MilestoneAdmin(admin.ModelAdmin):
    list_display  = ('title', 'created', 'date_due', 'progress', 'expired')
    list_filter   = ('project', 'date_due', 'closed')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = { models.TextField: {'widget' : CKEditor} }

class TicketAdmin(admin.ModelAdmin):
    list_display  = ('title', 'created', 'author', 'type', 'urgency', 'status', 'closed')
    list_filter   = ('project', 'type', 'urgency', 'status', 'closed', 'created')
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
    filter_horizontal = ('assignees',)
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Ticket, TicketAdmin)
