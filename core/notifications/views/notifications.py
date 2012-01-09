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

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.views import _get_user
from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from ..models import *
from ..forms import *

def _get_notification(request, *args, **kwargs):
    username = kwargs.get('username', None)
    id = kwargs.get('id', None)
    return get_object_or_404(Notification, user__username=username, id=id)

@permission_required('auth.change_user', _get_user)
@permission_required('notifications.view_notification')
def notification_list(request, username, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered notifications.
    """
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = SubscriptionsForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            form = SubscriptionsForm(user=user)
            messages.success(request, _("The user was updated successfully."))
    else:
        if Signature.objects.count() > 0:
            form = SubscriptionsForm(user=user)
        else:
            form = None

    return filtered_list_detail(
        request,
        Notification.objects.filter(user=user),
        fields=['title', 'created', 'read'],
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'form' : form,
            'object': user,
        },
        **kwargs
    )

@permission_required('auth.view_user', _get_user)
@permission_required('notifications.view_notification', _get_notification)
def notification_detail(request, username, id, **kwargs):
    """Displays the details of the selected notification.
    """
    user = get_object_or_404(User, username=username)
    notification = get_object_or_404(Notification, pk=id, user=user)

    if request.user == notification.user:
        notification.read = datetime.now()
        notification.save()

    object_list = Notification.objects.filter(user=user)

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        template_name='notifications/notification_detail.html',
        extra_context={'object_list': object_list},
        **kwargs
    )

@permission_required('auth.view_user', _get_user)
@permission_required('notifications.delete_notification', _get_notification)
def notification_delete(request, username, id, **kwargs):
    """Deletes an existing notification for the current user.
    """
    user = get_object_or_404(User, username=username)
    notification = get_object_or_404(Notification, pk=id, user=user)

    return create_update.delete_object(
        request,
        model=Notification,
        object_id=id,
        post_delete_redirect=reverse('notification_list', args=[user.username]),
        template_name='notifications/notification_delete.html',
        **kwargs
     )
