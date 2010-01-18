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

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q

from core.details import ModelDetails
from forms import AccountForm

@login_required
def index(request):
    """Show an account list.
    """
    accounts = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(username__startswith=token) | Q(username__endswith=token)

    if (queryset is not None):
        accounts = User.objects.filter(queryset)
    else:
        accounts = User.objects.all()
        
    return render_to_response('accounts/index.html', RequestContext(request, {'accounts': accounts}))

@login_required    
def add(request):
    """Add a new account.
    """
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return redirect_to(request, url='/accounts/view/%s/' % (account.pk))
    else:
        form = AccountForm()

    return render_to_response('accounts/add.html', RequestContext(request, {'form': form}))

@login_required    
def view(request, id):
    """Show account details.
    """
    account = get_object_or_404(User, pk=id)
    details = ModelDetails(instance=account)
    return render_to_response('accounts/view.html', RequestContext(request, {'account': account, 'details': details}))
    
@login_required 
def edit(request, id):
    """Edit an account.
    """
    account = User.objects.get(pk=id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/accounts/view/%s/' % (id))
    else:
        form = AccountForm(instance=account)
    return render_to_response('accounts/edit.html', RequestContext(request, {'account': account, 'form': form}))
 
@login_required   
def delete(request, id):
    """Delete an account.
    """
    account = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            account.delete()
            return redirect_to(request, url='/accounts/');
        return redirect_to(request, url='/accounts/view/%s/' % (id))
    return render_to_response('accounts/delete.html', RequestContext(request, {'account': account}))
