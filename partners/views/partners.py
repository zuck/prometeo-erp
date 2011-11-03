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

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to
from django.views.generic import list_detail, create_update
from django.template import RequestContext
from django.contrib import messages

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.addressing.views import *

from ..models import *
from ..forms import *

def _get_partner(request, *args, **kwargs):
    partner_id = kwargs.get('partner_id', None)
    id = kwargs.get('id', None)
    if partner_id:
        return get_object_or_404(Partner, id=partner_id)
    elif id:
        return get_object_or_404(Partner, id=id)
    return None

@permission_required('partners.change_partner')
def partner_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a partner list.
    """
    return filtered_list_detail(
        request,
        Partner,
        fields=['name', 'is_managed', 'is_supplier', 'is_customer', 'lead_status', 'vat_number', 'email'],
        page=page,
        paginate_by=paginate_by,
        template_name='partners/partner_list.html',
        **kwargs
    )

@permission_required('partners.add_partner')     
def partner_add(request, **kwargs):
    """Adds a new partner.
    """
    default_is_managed = (Partner.objects.filter(is_managed=True).count() == 0)
    default_assignee = request.user
    if default_is_managed:
        default_assignee = None

    partner = Partner(author=request.user, assignee=default_assignee, is_managed=default_is_managed)  
      
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, _("The partner has been saved."))
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = PartnerForm(instance=partner)

    return render_to_response('partners/partner_edit.html', RequestContext(request, {'form': form, 'object': partner}))

@permission_required('partners.change_partner', _get_partner)     
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

@permission_required('partners.change_partner', _get_partner)     
def partner_edit(request, id, **kwargs):
    """Edits a partner.
    """
    return create_update.update_object(
        request,
        object_id=id,
        form_class=PartnerForm,
        template_name='partners/partner_edit.html'
    )

@permission_required('partners.delete_partner', _get_partner)    
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

@permission_required('partners.change_partner', _get_partner) 
def partner_addresses(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the partner's addresses.
    """
    partner = get_object_or_404(Partner, pk=id)

    return address_list(
        request,
        owner=partner,
        page=page,
        paginate_by=paginate_by,
        template_name='partners/partner_addresses.html',
        extra_context={'object': partner, 'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)
def partner_add_address(request, id, **kwargs):
    """Adds a new address to the given partner.
    """
    return address_add(
        request,
        owner=get_object_or_404(Partner, pk=id),
        post_save_redirect=reverse('partner_addresses', args=[id]),
        template_name='partners/address_edit.html',
        extra_context={'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)
def partner_edit_address(request, partner_id, id, **kwargs):
    """Edits an address of the given partner.
    """
    partner = get_object_or_404(Partner, pk=partner_id)

    return address_edit(
        request,
        object_id=id,
        post_save_redirect=reverse('partner_addresses', args=[id]),
        template_name='partners/address_edit.html',
        extra_context={'owner': partner, 'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)
def partner_delete_address(request, partner_id, id, **kwargs):
    """Deletes an address of the given partner.
    """
    partner = get_object_or_404(Partner, pk=partner_id)

    return address_delete(
        request,
        object_id=id,
        post_delete_redirect=reverse('partner_addresses', args=[id]),
        template_name='partners/address_delete.html',
        extra_context={'owner': partner, 'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)  
def partner_phones(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the partner's phone numbers.
    """
    partner = get_object_or_404(Partner, pk=id)

    return phone_number_list(
        request,
        owner=partner,
        page=page,
        paginate_by=paginate_by,
        template_name='partners/partner_phones.html',
        extra_context={'object': partner, 'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)   
def partner_add_phone(request, id, **kwargs):
    """Adds a new phone number to the given partner.
    """
    return phone_number_add(
        request,
        owner=get_object_or_404(Partner, pk=id),
        post_save_redirect=reverse('partner_phones', args=[id]),
        template_name='partners/phone_edit.html',
        extra_context={'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)
def partner_edit_phone(request, partner_id, id, **kwargs):
    """Edits a phone number of the given partner.
    """
    partner = get_object_or_404(Partner, pk=partner_id)

    return phone_number_edit(
        request,
        object_id=id,
        post_save_redirect=reverse('partner_phones', args=[id]),
        template_name='partners/phone_edit.html',
        extra_context={'owner': partner, 'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)
def partner_delete_phone(request, partner_id, id, **kwargs):
    """Deletes a phone number of the given partner.
    """
    partner = get_object_or_404(Partner, pk=partner_id)

    return phone_number_delete(
        request,
        object_id=id,
        post_delete_redirect=reverse('partner_phones', args=[id]),
        template_name='partners/phone_delete.html',
        extra_context={'owner': partner, 'owner_class': Partner.__name__}
    )

@permission_required('partners.change_partner', _get_partner)
@permission_required('partners.change_contact')    
def partner_contacts(request, id, page=0, paginate_by=10, **kwargs):
    """Shows the partner's contacts.
    """
    partner = get_object_or_404(Partner, pk=id)

    return filtered_list_detail(
        request,
        partner.job_set.all(),
        exclude=['id', 'partner'],
        paginate_by=paginate_by,
        page=page,
        extra_context={'object': partner},
        template_name='partners/partner_contacts.html'
    )

@permission_required('partners.change_partner', _get_partner)
@permission_required('partners.add_contact')    
def partner_add_contact(request, id, **kwargs):
    """Adds a new contact to the given partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    instance = Job(partner=partner)

    if request.method == 'POST':
        form = PartnerJobForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _("Contact added to %s") % partner)
            return redirect_to(request, url=reverse("partner_contacts", args=[id]))
    else:
        form = PartnerJobForm(instance=instance)

    return render_to_response('partners/job_edit.html', RequestContext(request, {'form': form, 'object': instance}))
