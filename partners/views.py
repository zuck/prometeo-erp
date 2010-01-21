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
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q

from prometeo.core.details import ModelDetails

from models import Partner
from forms import PartnerForm

@login_required 
def index(request):
    """Show a partner list.
    """
    partners = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        partners = Partner.objects.filter(queryset)
    else:
        partners = Partner.objects.all()
        
    return render_to_response('partners/index.html', RequestContext(request, {'partners': partners}))
 
@login_required    
def add(request):
    """Add a new partner.
    """
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save()
            return redirect_to(request, url='/partners/view/%s/' % (partner.pk))
    else:
        form = PartnerForm()

    return render_to_response('partners/add.html', RequestContext(request, {'form': form}));

@login_required     
def view(request, id):
    """Show partner details.
    """
    partner = get_object_or_404(Partner, pk=id)
    details = ModelDetails(instance=partner)
    return render_to_response('partners/view.html', RequestContext(request, {'partner': partner, 'details': details}))

@login_required     
def edit(request, id):
    """Edit a partner.
    """
    partner = Partner.objects.get(pk=id)
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            return redirect_to(request, url='/partners/view/%s/' % (id))
    else:
        form = PartnerForm(instance=partner)
    return render_to_response('partners/edit.html', RequestContext(request, {'partner': partner, 'form': form}))

@login_required    
def delete(request, id):
    """Delete a partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            partner.delete()
            return redirect_to(request, url='/partners/');
        return redirect_to(request, url='/partners/view/%s/' % (id))
    return render_to_response('partners/delete.html', RequestContext(request, {'partner': partner}))
