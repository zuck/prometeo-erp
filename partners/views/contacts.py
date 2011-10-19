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

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.utils import clean_referer
from prometeo.core.views import filtered_list_detail
from prometeo.addressing.views import *

from ..models import *
from ..forms import *

def _get_contact(request, *args, **kwargs):
    contact_id = kwargs.get('contact_id', None)
    id = kwargs.get('id', None)
    if contact_id:
        return get_object_or_404(Contact, id=contact_id)
    elif id:
        return get_object_or_404(Contact, id=id)
    return None

@permission_required('partners.change_contact')
def contact_list(request, page=0, paginate_by=10, **kwargs):
    """Show all registered contacts.
    """
    return filtered_list_detail(
        request,
        Contact,
        exclude=['language', 'timezone', 'url', 'notes', 'user'],
        paginate_by=paginate_by,
        page=page,
        **kwargs
    )

@permission_required('partners.add_contact')     
def contact_add(request, **kwargs):
    """Adds a new contact.
    """
    referer = clean_referer(request)
    if referer == reverse("contact_list"):
        referer = None

    return create_update.create_object(
        request,
        form_class=ContactForm,
        post_save_redirect=referer,
        template_name='partners/contact_edit.html'
    )

@permission_required('partners.change_contact', _get_contact)     
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

@permission_required('partners.change_contact', _get_contact)     
def contact_edit(request, id, **kwargs):
    """Edits a contact.
    """
    return create_update.update_object(
        request,
        object_id=id,
        form_class=ContactForm,
        template_name='partners/contact_edit.html'
    )

@permission_required('partners.delete_contact', _get_contact)    
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

@permission_required('partners.change_contact', _get_contact)   
def contact_addresses(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the contact's addresses.
    """
    contact = get_object_or_404(Contact, pk=id)

    return address_list(
        request,
        owner=contact,
        page=page,
        paginate_by=paginate_by,
        template_name='partners/contact_addresses.html',
        extra_context={'object': contact, 'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)
def contact_add_address(request, id, **kwargs):
    """Adds a new address to the given partner.
    """
    return address_add(
        request,
        owner=get_object_or_404(Contact, pk=id),
        post_save_redirect=reverse('contact_addresses', args=[id]),
        template_name='partners/address_edit.html',
        extra_context={'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)
def contact_edit_address(request, contact_id, id, **kwargs):
    """Edits an address of the given contact.
    """
    contact = get_object_or_404(Contact, pk=contact_id)

    return address_edit(
        request,
        object_id=id,
        post_save_redirect=reverse('contact_addresses', args=[id]),
        template_name='partners/address_edit.html',
        extra_context={'owner': contact, 'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)
def contact_delete_address(request, contact_id, id, **kwargs):
    """Deletes an address of the given contact.
    """
    contact = get_object_or_404(Contact, pk=contact_id)

    return address_delete(
        request,
        object_id=id,
        post_delete_redirect=reverse('contact_addresses', args=[id]),
        template_name='partners/address_delete.html',
        extra_context={'owner': contact, 'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)  
def contact_phones(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the contact's phone numbers.
    """
    contact = get_object_or_404(Contact, pk=id)

    return phone_number_list(
        request,
        owner=contact,
        page=page,
        paginate_by=paginate_by,
        template_name='partners/contact_phones.html',
        extra_context={'object': contact, 'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)   
def contact_add_phone(request, id, **kwargs):
    """Adds a new phone number to the given contact.
    """
    return phone_number_add(
        request,
        owner=get_object_or_404(Contact, pk=id),
        post_save_redirect=reverse('contact_phones', args=[id]),
        template_name='partners/phone_edit.html',
        extra_context={'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)
def contact_edit_phone(request, contact_id, id, **kwargs):
    """Edits a phone number of the given contact.
    """
    contact = get_object_or_404(Contact, pk=contact_id)

    return phone_number_edit(
        request,
        object_id=id,
        post_save_redirect=reverse('contact_phones', args=[id]),
        template_name='partners/phone_edit.html',
        extra_context={'owner': contact, 'owner_class': Contact.__name__}
    )

@permission_required('partners.change_contact', _get_contact)
def contact_delete_phone(request, contact_id, id, **kwargs):
    """Deletes a phone number of the given contact.
    """
    contact = get_object_or_404(Contact, pk=contact_id)

    return phone_number_delete(
        request,
        object_id=id,
        post_delete_redirect=reverse('contact_phones', args=[id]),
        template_name='partners/phone_delete.html',
        extra_context={'owner': contact, 'owner_class': Contact.__name__}
    )

@permission_required('partners.change_partner')
@permission_required('partners.change_contact', _get_contact)    
def contact_jobs(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the contact's jobs.
    """
    contact = get_object_or_404(Contact, pk=id)

    return filtered_list_detail(
        request,
        contact.job_set.all(),
        exclude=['id', 'contact'],
        paginate_by=paginate_by,
        page=page,
        extra_context={'object': contact},
        template_name='partners/contact_jobs.html'
    )

@permission_required('partners.change_partner')
@permission_required('partners.add_contact')    
def contact_add_job(request, id, **kwargs):
    """Adds a new job to the given contact.
    """
    contact = get_object_or_404(Contact, pk=id)
    instance = Job(contact=contact)

    if request.method == 'POST':
        form = ContactJobForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _("Contact added to %s") % instance.partner)
            return redirect_to(request, url=reverse("contact_jobs", args=[instance.contact_id]))
    else:
        form = ContactJobForm(instance=instance)

    return render_to_response('partners/job_edit.html', RequestContext(request, {'object': instance, 'form': form}))

@permission_required('partners.change_partner')
@permission_required('partners.change_contact', _get_contact)
def contact_edit_job(request, contact_id, id, **kwargs):
    """Edits a job of the given contact.
    """
    instance = get_object_or_404(Job, id=id, contact__id=contact_id)

    if request.method == 'POST':
        form = ContactJobForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _("Contact updated") % instance.partner)
            return redirect_to(request, url=reverse("contact_jobs", args=[instance.contact_id]))
    else:
        form = ContactJobForm(instance=instance)

    return render_to_response('partners/job_edit.html', RequestContext(request, {'object': instance, 'form': form}))

@permission_required('partners.change_partner')
@permission_required('partners.delete_contact', _get_contact)
def contact_delete_job(request, contact_id, id, **kwargs):
    """Deletes a job of the given contact.
    """
    job = get_object_or_404(Job, id=id, contact__id=contact_id)

    return create_update.delete_object(
        request,
        model=Job,
        object_id=id,
        post_delete_redirect=reverse('contact_jobs', args=[contact_id]),
        template_name='partners/job_delete.html',
        **kwargs
    )
