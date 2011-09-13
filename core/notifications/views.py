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

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.conf import settings

from prometeo.core.filter import filter_objects

from models import *

@permission_required('notifications.change_notification') 
def notification_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered notifications.
    """
    object_list = Notification.objects.filter(user=request.user)

    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Notification,
                                                fields=['id', 'title', 'created', 'read'],
                                                object_list=object_list
                                              )

    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': request.user,
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        **kwargs
    )

@permission_required('notifications.change_notification') 
def notification_detail(request, id, **kwargs):
    """Displays the details of the selected notification.
    """
    notification = get_object_or_404(Notification, pk=id)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('notifications.change_notification') or request.user == notification.user)):
        messages.error(request, _("You can't view this notification's detials."))
        return redirect_to(request, url=reverse('user_login'))

    if request.user == notification.user:
        notification.read = datetime.now()
        notification.save()

    object_list = Notification.objects.all()

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        template_name='notifications/notification_detail.html',
        extra_context={'object_list': object_list},
        **kwargs
    )
