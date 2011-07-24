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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import permission_required

from prometeo.core.filter import filter_objects

from models import *
from forms import *

@permission_required('auth.change_user') 
def set_language(request):
    """Set the current language.
    """
    lang_code = request.user.get_profile().language
    if lang_code and check_for_language(lang_code):
        request.session['django_language'] = lang_code

@permission_required('auth.change_user') 
def user_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all active users.
    """
    filter_fields, object_list = filter_objects(request, User, object_list=User.objects.filter(is_active=True))
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        template_name='auth/user_list.html',
        extra_context={'filter_fields': filter_fields},
        **kwargs
    )
  
def user_detail(request, username, **kwargs):
    """Displays a user's profile.
    """
    user = get_object_or_404(User, username=username, is_active=True)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('auth.change_user') or request.user.username == username)):
        messages.error(request, _("You can't view this user's profile."))
        return redirect_to(request, url=reverse('user_login'))

    return list_detail.object_detail(
        request,
        slug=username,
        slug_field='username',
        queryset=User.objects.filter(is_active=True),
        template_name='auth/user_detail.html',
        **kwargs
    )
 
@permission_required('auth.add_user')    
def user_add(request, **kwargs):
    """Adds a new user's profile.
    """
    user = User()  
      
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            messages.success(request, _("The user's profile has been saved."))
            return redirect_to(request, url=user.get_absolute_url())
    else:
        form = UserEditForm(instance=user)

    return render_to_response('auth/user_edit.html', RequestContext(request, {'form': form, 'object': user}))
  
def user_edit(request, username, **kwargs):
    """Edits a user's profile.
    """
    user = get_object_or_404(User, username=username, is_active=True)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('auth.change_user') or request.user.username == username)):
        messages.error(request, _("You can't edit this user's profile."))
        return redirect_to(request, url=reverse('user_login'))
        
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, _("The user's profile has been updated."))
            return redirect_to(request, url=user.get_absolute_url())
    else:
        form = UserEditForm(instance=user)

    return render_to_response('auth/user_edit.html', RequestContext(request, {'form': form, 'object': user}))
  
def user_delete(request, username, **kwargs):
    """Deletes a user's profile.
    """ 
    user = get_object_or_404(User, username=username, is_active=True)
    
    if not (request.user.is_authenticated() and (request.user.has_perm('auth.delete_user') or request.user.username == username)):
        messages.error(request, _("You can't delete this user's profile."))
        return redirect_to(request, url=user.get_absolute_url())
        
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

