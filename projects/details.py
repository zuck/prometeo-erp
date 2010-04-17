#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from prometeo.core import details

class MilestoneListDetails(details.ModelPaginatedListDetails):
    def row_template(self, row, index):
        i = self._header.index('date completed')
        dc = row[i]
        
        if dc != None:
            return u'\t<tr class="completed">\n'
            
        j = self._header.index('date due')
        dd = row[j]
        if dd is not None and dd < datetime.now():
            return u'\t<tr class="expired">\n'
            
        return u'\t<tr>\n'
                
class TicketListDetails(details.ModelPaginatedListDetails):  
    def row_template(self, row, index):
        i = self._header.index('urgency')
        value = details.value_to_string(row[i])
        
        if value == _('low'):
            return u'\t<tr class="low">\n'
            
        elif value == _('medium'):
            return u'\t<tr class="medium">\n'
            
        elif value == _('high'):
            return u'\t<tr class="high">\n'
            
        elif value == _('critical'):
            return u'\t<tr class="critical">\n'
            
class TimelineListDetails(details.ModelPaginatedListDetails):
    def __init__(self, request, queryset=[]):
        super(TimelineListDetails, self).__init__(request, queryset, fields=[], with_actions=False)
        self._header = []
        self._rows = []
        self._header.append(_('event'))
        for i, instance in enumerate(queryset):
            self._rows.append(['%s' % instance,])
            
    def table_template(self):
        return u'<table class="list">\n'
