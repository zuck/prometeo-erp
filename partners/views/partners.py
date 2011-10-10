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

from prometeo.core.utils import filter_objects
from prometeo.addressing.forms import *

from ..models import *
from ..forms import *

@permission_required('partners.change_partner')
def partner_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a partner list.
    """
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                Partner,
                                                fields=['name', 'vat_number', 'is_managed', 'is_supplier', 'is_customer', 'vat', 'email'],
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

@permission_required('partners.add_partner')     
def partner_add(request, **kwargs):
    """Adds a new partner.
    """
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save()
            messages.success(request, _("Partner added"))
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = PartnerForm(initial={'assignee': request.user})

    return render_to_response('partners/partner_edit.html', RequestContext(request, {'form': form}))

@permission_required('partners.change_partner')     
def partner_detail(request, id, page=None, **kwargs):
    """Shows partner details.
    """
    object_list = Partner.objects.all()
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        **kwargs
    )

@permission_required('partners.change_partner')     
def partner_edit(request, id, **kwargs):
    """Edits a partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, _("Partner updated"))
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = PartnerForm(instance=partner)
    return render_to_response('partners/partner_edit.html', RequestContext(request, {'object': partner, 'form': form}))

@permission_required('partners.delete_partner')    
def partner_delete(request, id, **kwargs):
    """Deletes a partner.
    """
    return create_update.delete_object(
            request,
            model=Partner,
            object_id=id,
            post_delete_redirect=reverse('partner_list'),
            template_name='partners/partner_delete.html',
            **kwargs
        )

@permission_required('partners.change_partner')
@permission_required('addressing.change_address')    
def partner_addresses(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the partner's addresses.
    """
    partner = get_object_or_404(Partner, pk=id)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                partner.addresses.all(),
                                                exclude=['id', 'content_object']
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': partner,
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        template_name='partners/partner_addresses.html',
        **kwargs
    )

@permission_required('partners.change_partner')
@permission_required('addressing.add_address')    
def partner_add_address(request, id, **kwargs):
    """Adds a new address to the given partner.
    """
    partner = get_object_or_404(Partner, pk=id)

    if request.method == 'POST':
        form = AddressForm(request.POST, content_object=partner)
        if form.is_valid():
            form.save()
            messages.success(request, _("Address added to %s") % partner)
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = AddressForm(content_object=partner)

    return render_to_response('partners/address_edit.html', RequestContext(request, {'form': form}))

@permission_required('partners.change_partner')
@permission_required('addressing.change_phone_number')    
def partner_phones(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the partner's phone numbers.
    """
    partner = get_object_or_404(Partner, pk=id)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                partner.phone_numbers.all(),
                                                exclude=['id', 'content_object']
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': partner,
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        template_name='partners/partner_phones.html',
        **kwargs
    )

@permission_required('partners.change_partner')
@permission_required('addressing.add_phone_number')    
def partner_add_phone(request, id, **kwargs):
    """Adds a new phone number to the given partner.
    """
    partner = get_object_or_404(Partner, pk=id)

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST, content_object=partner)
        if form.is_valid():
            form.save()
            messages.success(request, _("Phone number added to %s") % partner)
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = PhoneNumberForm(content_object=partner)

    return render_to_response('partners/phone_edit.html', RequestContext(request, {'form': form}))

@permission_required('partners.change_partner')
@permission_required('partners.change_contact')    
def partner_contacts(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the partner's contacts.
    """
    partner = get_object_or_404(Partner, pk=id)
    field_names, filter_fields, object_list = filter_objects(
                                                request,
                                                partner.job_set.all(),
                                                exclude=['id', 'partner']
                                              )
    return list_detail.object_list(
        request,
        queryset=object_list,
        paginate_by=paginate_by,
        page=page,
        extra_context={
            'object': partner,
            'field_names': field_names,
            'filter_fields': filter_fields,
        },
        template_name='partners/partner_contacts.html',
        **kwargs
    )

@permission_required('partners.change_partner')
@permission_required('partners.add_contact')    
def partner_add_contact(request, id, **kwargs):
    """Adds a new contact to the given partner.
    """
    partner = get_object_or_404(Partner, pk=id)

    if request.method == 'POST':
        form = PartnerJobForm(request.POST)
        if form.is_valid():
            job = form.save(False)
            job.partner = partner
            job.save()
            messages.success(request, _("Contact added to %s") % partner)
            return redirect_to(request, url=reverse("partner_contacts", args=[id]))
    else:
        form = PartnerJobForm()

    return render_to_response('partners/job_edit.html', RequestContext(request, {'form': form}))
