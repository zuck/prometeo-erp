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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.utils.translation import check_for_language
from django.template import RequestContext
from django.db.models import Q

from details import ModelDetails, ModelPaginatedListDetails, field_to_value
from models import *
from forms import *

class AccountDetails(ModelDetails):
    def __init__(self, instance, fields=[], exclude=['id']):
        field_list_user = [f for f in instance._meta.fields if len(fields) == 0 or f.attname in fields]
        field_list_profile = [f for f in instance.get_profile()._meta.fields if len(fields) == 0 or f.attname in fields]
        fields = [(f.verbose_name, field_to_value(f, instance)) for f in field_list_user if f.attname not in exclude]
        fields.extend([(f.verbose_name, field_to_value(f, instance.get_profile())) for f in field_list_profile if f.attname not in exclude])
        super(ModelDetails, self).__init__(fields)

def set_language(request):
    """Set the current language.
    """
    lang_code = request.user.get_profile().language
    if lang_code and check_for_language(lang_code):
        request.session['django_language'] = lang_code

def logged(request):
    response = HttpResponseRedirect('/')
    set_language(request)
    return response

def index(request):
    """Show an account list.
    """
    accounts = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(username__startswith=token) | Q(username__endswith=token)

    if (queryset is not None):
        accounts = Account.objects.filter(queryset)
    else:
        accounts = Account.objects.all()
        
    accounts = ModelPaginatedListDetails(request, accounts, exclude=['id', 'is_active', 'password', 'date_joined'])
        
    return render_to_response('accounts/index.html', RequestContext(request, {'accounts': accounts}))
    
def add(request):
    """Add a new account.
    """
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return redirect_to(request, url=account.get_absolute_url())
    else:
        form = AccountForm()

    return render_to_response('accounts/add.html', RequestContext(request, {'form': form}))
    
def view(request, id):
    """Show account details.
    """
    account = get_object_or_404(Account, pk=id)
    details = AccountDetails(instance=account, exclude=['id', 'password', 'is_active', 'user_id'])
    return render_to_response('accounts/view.html', RequestContext(request, {'account': account, 'details': details}))
     
def edit(request, id):
    """Edit an account.
    """
    account = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            set_language(request)
            return redirect_to(request, url='/accounts/view/%s/' % (id))
    else:
        form = AccountForm(instance=account)
    return render_to_response('accounts/edit.html', RequestContext(request, {'account': account, 'form': form}))
    
def delete(request, id):
    """Delete an account.
    """
    account = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            account.delete()
            return redirect_to(request, url='/accounts/');
        return redirect_to(request, url='/accounts/view/%s/' % (id))
    return render_to_response('accounts/delete.html', RequestContext(request, {'account': account}))

def start(request):
    """Start page.
    """
    return render_to_response('start.html', RequestContext(request))
