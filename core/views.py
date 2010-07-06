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

__author__ = 'Emanuele Bertoldi <zuck@fastwebnet.it>'
__copyright__ = 'Copyright (c) 2010 Emanuele Bertoldi'
__version__ = '$Revision$'

from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.utils.translation import check_for_language
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.contrib import messages

from prometeo.core.details import ModelDetails, ModelPaginatedListDetails, field_to_value
from prometeo.core.search import search

from models import *
from forms import *

def start(request):
    """Start page.
    """
    return render_to_response('start.html', RequestContext(request))

def set_language(request):
    """Set the current language.
    """
    lang_code = request.user.get_profile().language
    if lang_code and check_for_language(lang_code):
        request.session['django_language'] = lang_code

class AccountDetails(ModelDetails):
    def __init__(self, instance, fields=[], exclude=['id']):
        field_list_user = [f for f in instance._meta.fields if len(fields) == 0 or f.attname in fields]
        field_list_profile = [f for f in instance.get_profile()._meta.fields if len(fields) == 0 or f.attname in fields]
        fields = [(f.verbose_name, field_to_value(f, instance)) for f in field_list_user if f.attname not in exclude]
        fields.extend([(f.verbose_name, field_to_value(f, instance.get_profile())) for f in field_list_profile if f.attname not in exclude])
        super(ModelDetails, self).__init__(fields)
        
class PermissionListDetails(ModelPaginatedListDetails):
    def table_template(self):
        return u'<table class="list">\n'

def account_logged(request):
    response = HttpResponseRedirect('/')
    set_language(request)
    messages.success(request, _("Your are now logged"))
    return response

@permission_required('auth.change_account')
def account_index(request):
    """Show an account list.
    """    
    search_fields, accounts = search(request, Account, exclude=['id', 'is_active', 'is_staff', 'is_superuser', 'password', 'date_joined'])
        
    accounts = ModelPaginatedListDetails(request, accounts, exclude=['id', 'is_active', 'is_staff', 'is_superuser', 'password', 'date_joined'])
        
    return render_to_response('accounts/index.html', RequestContext(request, {'accounts': accounts, 'search_fields': search_fields}))
    
@permission_required('auth.add_user')
def account_add(request):
    """Add a new account.
    """
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, _("Account added"))
            return redirect_to(request, url=account.get_absolute_url())
    else:
        form = AccountForm()

    return render_to_response('accounts/add.html', RequestContext(request, {'form': form}))
    
@permission_required('auth.change_account')
def account_view(request, id, page=None):
    """Show account details.
    """
    account = get_object_or_404(Account, pk=id)
    
    # Groups.  
    if page == 'groups':
        groups = ModelPaginatedListDetails(request, account.groups.all(), with_actions=False)
        return render_to_response('accounts/groups.html', RequestContext(request, {'account': account, 'groups': groups}))
    
    # Permissions.  
    elif page == 'permissions':
        permissions = PermissionListDetails(request, account.user_permissions.all(), exclude=['id', 'content_type_id'], with_actions=False)
        return render_to_response('accounts/permissions.html', RequestContext(request, {'account': account, 'permissions': permissions}))
        
    # Details.
    details = AccountDetails(instance=account, exclude=['id', 'password', 'is_active', 'is_staff', 'is_superuser', 'user_id'])
    return render_to_response('accounts/view.html', RequestContext(request, {'account': account, 'details': details}))
    
@permission_required('auth.change_account')
def account_edit(request, id):
    """Edit an account.
    """
    account = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            set_language(request)
            messages.success(request, _("Account updated"))
            return redirect_to(request, url=account.get_absolute_url())
    else:
        form = AccountForm(instance=account)
    return render_to_response('accounts/edit.html', RequestContext(request, {'account': account, 'form': form}))
    
@permission_required('auth.delete_account')
def account_delete(request, id):
    """Delete an account.
    """
    account = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            account.delete()
            messages.success(request, _("Account deleted"))
            return redirect_to(request, url='/accounts/');
        return redirect_to(request, url=account.get_absolute_url())
    return render_to_response('accounts/delete.html', RequestContext(request, {'account': account}))
    
@permission_required('auth.change_group')
def group_index(request):
    """Show a group list.
    """    
    search_fields, groups = search(request, Group)
        
    groups = ModelPaginatedListDetails(request, groups)
        
    return render_to_response('accounts/groups/index.html', RequestContext(request, {'groups': groups, 'search_fields': search_fields}))
    
@permission_required('auth.add_group')
def group_add(request):
    """Add a new group.
    """
    if request.method == 'POST':
        form = AccountGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, _("Group added"))
            return redirect_to(request, url=group.get_absolute_url())
    else:
        form = AccountGroupForm()

    return render_to_response('accounts/groups/add.html', RequestContext(request, {'form': form}))

@permission_required('auth.change_group')   
def group_view(request, id, page=None):
    """Show group details.
    """
    group = get_object_or_404(AccountGroup, pk=id)
    
    # Permissions.  
    if page == 'permissions':
        permissions = PermissionListDetails(request, group.permissions.all(), exclude=['id', 'content_type_id'], with_actions=False)
        return render_to_response('accounts/groups/permissions.html', RequestContext(request, {'group': group, 'permissions': permissions}))
        
    # Details.
    details = ModelDetails(instance=group)
    return render_to_response('accounts/groups/view.html', RequestContext(request, {'group': group, 'details': details}))
    
@permission_required('auth.change_group')
def group_edit(request, id):
    """Edit a group.
    """
    group = get_object_or_404(AccountGroup, pk=id)
    if request.method == 'POST':
        form = AccountGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group updated"))
            return redirect_to(request, url=group.get_absolute_url())
    else:
        form = AccountGroupForm(instance=group)
    return render_to_response('accounts/groups/edit.html', RequestContext(request, {'group': group, 'form': form}))
  
@permission_required('auth.delete_group')
def group_delete(request, id):
    """Delete a group.
    """
    group = get_object_or_404(AccountGroup, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            group.delete()
            messages.success(request, _("Group deleted"))
            return redirect_to(request, url='/accounts/groups/');
        return redirect_to(request, url=group.get_absolute_url())
    return render_to_response('accounts/groups/delete.html', RequestContext(request, {'group': group}))
