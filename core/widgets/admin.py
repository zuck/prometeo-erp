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

from django.contrib import admin

from models import *
from forms import WidgetTemplateForm
    
class WidgetInlineAdmin(admin.StackedInline):
    model = Widget

class RegionAdmin(admin.ModelAdmin):
    list_display  = ('slug', 'description')
    inlines = [WidgetInlineAdmin,]

class WidgetTemplateAdmin(admin.ModelAdmin):
    form = WidgetTemplateForm
    list_display  = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

class WidgetAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display  = ('__unicode__',)
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Region, RegionAdmin)
admin.site.register(WidgetTemplate, WidgetTemplateAdmin)
admin.site.register(Widget, WidgetAdmin)
