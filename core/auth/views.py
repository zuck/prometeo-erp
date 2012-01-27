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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.comments.models import *
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail, set_language

from models import *
from forms import *

def _adapt_form(request, form):
    if not request.user.has_perm('auth.change_group'):
        del form.fields['groups']

    if not request.user.has_perm('auth.change_permission'):
        del form.fields['user_permissions']
        
    if not request.user.is_superuser:
        del form.fields['is_staff']
        del form.fields['is_active']
        del form.fields['is_superuser']

def _get_user(request, *args, **kwargs):
    username = kwargs.get('username', None)
    return get_object_or_404(User, username=username)

def _get_comment(request, *args, **kwargs):
    id = kwargs.get('id', None)
    return get_object_or_404(Comment, id=id, site__pk=settings.SITE_ID)

def user_logged(request):
    """Sets the language selected by the logged user.
    """
    lang = request.user.get_profile().language
    return set_language(request, lang)

@permission_required('auth.view_user') 
def user_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all active users.
    """
    return filtered_list_detail(
        request,
        MyUser.objects.all(),
        fields=['username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'last_login'],
        paginate_by=paginate_by,
        page=page,
        template_name='auth/user_list.html',
        **kwargs
    )

@permission_required('auth.view_user', _get_user)  
def user_detail(request, username, **kwargs):
    """Displays a user's profile.
    """
    object_list = MyUser.objects.all()
    return list_detail.object_detail(
        request,
        slug=username,
        slug_field='username',
        queryset=object_list,
        template_name='auth/user_detail.html',
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('auth.add_user')    
def user_add(request, **kwargs):
    """Adds a new user's profile.
    """
    user = User(is_active=True)  
      
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        _adapt_form(request, form)
        if form.is_valid():
            form.save()
            messages.success(request, _("The user was created successfully."))
            return redirect_to(request, url=user.get_absolute_url())
    else:
        form = UserEditForm(instance=user)
        _adapt_form(request, form)

    return render_to_response('auth/user_edit.html', RequestContext(request, {'form': form, 'object': user}))

@permission_required('auth.change_user', _get_user)   
def user_edit(request, username, **kwargs):
    """Edits a user's profile.
    """
    user = get_object_or_404(User, username=username)
        
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        _adapt_form(request, form)
        pform = UserProfileForm(request.POST, instance=user.get_profile())
        if form.is_valid() and pform.is_valid():
            user = form.save()
            profile = pform.save()
            if request.user == user:
                set_language(request, profile.language)
            messages.success(request, _("The user was updated successfully."))
            return redirect_to(request, url=user.get_absolute_url())
    else:
        form = UserEditForm(instance=user)
        _adapt_form(request, form)
        pform = UserProfileForm(instance=user.get_profile())

    return render_to_response('auth/user_edit.html', RequestContext(request, {'form': form, 'pform': pform, 'object': user}))

@permission_required('auth.delete_user', _get_user)  
def user_delete(request, username, **kwargs):
    """Deletes a user's profile.
    """ 
    user = get_object_or_404(User, username=username)
        
    if request.method == 'POST' and user == request.user:
        logout(request)

    return create_update.delete_object(
            request,
            model=User,
            slug=user.username,
            slug_field='username',
            post_delete_redirect='/users/',
            template_name='auth/user_delete.html',
            **kwargs
        )

@permission_required('comments.delete_comment', _get_comment)  
def comment_delete(request, id, **kwargs):
    """Deletes a user's comment.
    """ 
    comment = get_object_or_404(Comment, id=id, site__pk=settings.SITE_ID)
    return create_update.delete_object(
            request,
            model=Comment,
            object_id=id,
            post_delete_redirect=comment.content_object.get_absolute_url(),
            template_name='auth/comment_delete.html',
            **kwargs
        )
