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
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from models import *
from forms import *

def _get_content_type_by(name):
    model_name = name
    if name[-1] == 's':
        model_name = name[:-1]
    return ContentType.objects.get(model=model_name)

def _get_object_by(object_model, object_id):
    content_type = _get_content_type_by(object_model)
    model_class = content_type.model_class()
    return get_object_or_404(model_class, pk=object_id)  

def _get_object_view_perm(request, *args, **kwargs):
    object_model = kwargs.get('object_model', None)
    content_type = _get_content_type_by(object_model)
    app_label = content_type.app_label
    model_name = content_type.model
    return "%s.view_%s" % (app_label, model_name)

def _get_object(request, *args, **kwargs):
    object_model = kwargs.get('object_model', None)
    object_id = kwargs.get('object_id', None)
    return _get_object_by(object_model, object_id)

def _get_notification(request, *args, **kwargs):
    id = kwargs.get('id', None)
    return get_object_or_404(Notification, pk=id)

@permission_required(_get_object_view_perm, _get_object)
def object_follow(request, object_model, object_id, path='/', **kwargs):
    """The current user starts to follow object's activies.
    """
    obj = _get_object_by(object_model, object_id)
    follower = request.user
    
    if isinstance(obj, Observable):
        obj.follow(follower)
        messages.success(request, _("%s is now following %s.") % (follower, obj))

    return redirect_to(request, permanent=False, url=path)

@permission_required(_get_object_view_perm, _get_object)
def object_unfollow(request, object_model, object_id, path='/', **kwargs):
    """The current user stops to follow object's activies.
    """
    obj = _get_object_by(object_model, object_id)
    follower = request.user

    if isinstance(obj, Observable):
        obj.unfollow(follower)
        messages.success(request, _("%s doesn't follow %s anymore.") % (follower, obj))

    return redirect_to(request, permanent=False, url=path)

@permission_required(_get_object_view_perm, _get_object)
@permission_required('notifications.view_notification')
def notification_list(request, object_model, object_id, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered notifications.
    """
    obj = _get_object_by(object_model, object_id)
    
    if request.method == 'POST':
        form = SubscriptionsForm(request.POST, subscriber=obj)
        if form.is_valid():
            form.save()
            form = SubscriptionsForm(subscriber=obj)
            messages.success(request, _("Subscriptions for %s were updated successfully.") % obj)
    else:
        if Signature.objects.count() > 0:
            form = SubscriptionsForm(subscriber=obj)
        else:
            form = None

    return filtered_list_detail(
        request,
        Notification.objects.filter(target=obj),
        fields=['title', 'created', 'read'],
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'form' : form,
            'object': obj,
        },
        **kwargs
    )

@permission_required(_get_object_view_perm, _get_object)
@permission_required('notifications.view_notification', _get_notification)
def notification_detail(request, object_model, object_id, id, **kwargs):
    """Displays the details of the selected notification.
    """
    obj = _get_object_by(object_model, object_id)
    notification = get_object_or_404(Notification, target=obj, pk=id)
    
    notification.read = datetime.now()
    notification.save()

    object_list = Notification.objects.filter(target=notification.target)

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        template_name='notifications/notification_detail.html',
        extra_context={'object_list': object_list},
        **kwargs
    )

@permission_required('notifications.delete_notification', _get_notification)
def notification_delete(request, object_model, object_id, id, **kwargs):
    """Deletes an existing notification for the current user.
    """
    obj = _get_object_by(object_model, object_id)
    notification = get_object_or_404(Notification, target=obj, pk=id)

    return create_update.delete_object(
        request,
        model=Notification,
        object_id=id,
        post_delete_redirect=reverse('notification_list', args=[notification.target._meta.verbose_name_plural, notification.target_id]),
        template_name='notifications/notification_delete.html',
        **kwargs
     )
