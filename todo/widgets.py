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

from datetime import date

from models import *

def latest_tasks(context):
    try:
        count = context['count']
    except KeyError:
        count = 5
    request = context['request']
    context['object_list'] = Task.objects.filter(user=request.user)[0:count]
    return context

def today_tasks(context):
    request = context['request']
    context['object_list'] = Task.objects.filter(user=request.user, start_date=date.today())
    return context
