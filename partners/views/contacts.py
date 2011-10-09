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

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to
from django.views.generic import list_detail, create_update
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from prometeo.core.utils import filter_objects, clean_referer

from ..models import *
from ..forms import *

@permission_required('partners.change_contact')
def contact_list(request, page=0, paginate_by=10, **kwargs):
    """Show all registered contacts.
    """
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Contact,
                                                exclude=['language', 'timezone', 'url', 'notes', 'user']
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        **kwargs
    )

@permission_required('partners.add_contact')     
def contact_add(request, **kwargs):
    """Adds a new contact.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, _("Contact added"))
            referer = clean_referer(request)
            if referer == reverse("contact_list"):
                referer = contact.get_absolute_url()
            return redirect_to(request, url=referer)
    else:
        form = ContactForm()

    return render_to_response('partners/contact_edit.html', RequestContext(request, {'form': form}))

@permission_required('partners.change_contact')     
def contact_detail(request, id, page=None, **kwargs):
    """Shows contact details.
    """
    object_list = Contact.objects.all()
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        **kwargs
    )

@permission_required('partners.change_contact')     
def contact_edit(request, id, **kwargs):
    """Edits a contact.
    """
    contact = get_object_or_404(Contact, pk=id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, _("Contact updated"))
            return redirect_to(request, url=contact.get_absolute_url())
    else:
        form = ContactForm(instance=contact)
    return render_to_response('partners/contact_edit.html', RequestContext(request, {'object': contact, 'form': form}))

@permission_required('partners.delete_contact')    
def contact_delete(request, id, **kwargs):
    """Deletes a contact.
    """
    return create_update.delete_object(
            request,
            model=Contact,
            object_id=id,
            post_delete_redirect=reverse('contact_list'),
            template_name='partners/contact_delete.html',
            **kwargs
        )

@permission_required('partners.change_partner')
@permission_required('partners.change_contact')    
def contact_jobs(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the contact's jobs.
    """
    contact = get_object_or_404(Contact, pk=id)

    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                contact.job_set.all(),
                                                exclude=['id', 'contact']
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': contact,
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        template_name='partners/contact_jobs.html',
        **kwargs
    )

@permission_required('partners.change_partner')
@permission_required('partners.add_contact')    
def contact_add_job(request, id, **kwargs):
    """Adds a new job to the given contact.
    """
    contact = get_object_or_404(Contact, pk=id)

    if request.method == 'POST':
        form = ContactJobForm(request.POST)
        if form.is_valid():
            job = form.save(False)
            job.contact = contact
            job.save()
            messages.success(request, _("Contact added to %s") % job.partner)
            return redirect_to(request, url=reverse("contact_jobs", args=[id]))
    else:
        form = ContactJobForm()

    return render_to_response('partners/job_edit.html', RequestContext(request, {'form': form}))
