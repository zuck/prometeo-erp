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

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.db.models import Q

from prometeo.core.details import ModelDetails, ModelPaginatedListDetails, value_to_string
from prometeo.core.paginator import paginate

from models import *
from forms import *
from details import *

@permission_required('partners.change_partner')
def partner_index(request):
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
        
    partners = PartnerListDetails(request, partners)
        
    return render_to_response('partners/index.html', RequestContext(request, {'partners': partners}))

@permission_required('partners.add_partner')     
def partner_add(request):
    """Add a new partner.
    """
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save()
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = PartnerForm()

    return render_to_response('partners/add.html', RequestContext(request, {'form': form}));

@permission_required('partners.change_partner')     
def partner_view(request, id, page=None):
    """Show partner details.
    """
    partner = get_object_or_404(Partner, pk=id)
    
    # Contacts.
    if page == 'contacts':
        contacts = ContactJobListDetails(request, partner.job_set.select_related(), exclude=['id', 'url', 'email'])
        return render_to_response('partners/contacts.html', RequestContext(request, {'partner': partner, 'contacts': contacts}))
    
    # Addresses.
    if page == 'addresses':
        addresses = PartnerAddressListDetails(partner.pk, request, partner.addresses.select_related(), exclude=['id'])
        return render_to_response('partners/addresses.html', RequestContext(request, {'partner': partner, 'addresses': addresses}))
    
    # Telephones.
    if page == 'telephones':
        telephones = PartnerTelephoneListDetails(partner.pk, request, partner.telephones.select_related(), exclude=['id'])
        return render_to_response('partners/telephones.html', RequestContext(request, {'partner': partner, 'telephones': telephones}))
    
    # Details.
    details = PartnerDetails(instance=partner)
    return render_to_response('partners/view.html', RequestContext(request, {'partner': partner, 'details': details}))

@permission_required('partners.change_partner')     
def partner_edit(request, id):
    """Edit a partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=partner.get_absolute_url())
    else:
        form = PartnerForm(instance=partner)
    return render_to_response('partners/edit.html', RequestContext(request, {'partner': partner, 'form': form}))

@permission_required('partners.delete_partner')    
def partner_delete(request, id):
    """Delete a partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            partner.delete()
            return redirect_to(request, url='/partners/');
        return redirect_to(request, url=partner.get_absolute_url())
    return render_to_response('partners/delete.html', RequestContext(request, {'partner': partner}))
    
@permission_required('partners.change_partner')
def partner_suppliers(request):
    """Show a supplier list.
    """
    partners = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)
        
    partners = Partner.objects.filter(supplier=True)

    if (queryset is not None):
        partners = partners.filter(queryset)
        
    partners = PartnerListDetails(request, partners, exclude=['id', 'customer', 'supplier'])
        
    return render_to_response('partners/suppliers.html', RequestContext(request, {'partners': partners}))
    
@permission_required('partners.change_partner')
def partner_customers(request):
    """Show a customer list.
    """
    partners = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)
        
    partners = Partner.objects.filter(customer=True)

    if (queryset is not None):
        partners = partners.filter(queryset)
        
    partners = PartnerListDetails(request, partners, exclude=['id', 'customer', 'supplier'])
        
    return render_to_response('partners/customers.html', RequestContext(request, {'partners': partners}))
    
@permission_required('partners.change_partner')
def partner_add_telephone(request, id):
    """Add a new telephone number for the partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    
    if request.method == 'POST':
        form = PartnerTelephoneForm(request.POST)
        if form.is_valid():
            telephone = form.save()
            partner.telephones.add(telephone)
            return redirect_to(request, url=partner.get_telephones_url())
    else:
        form = PartnerTelephoneForm()

    return render_to_response('partners/add_telephone.html', RequestContext(request, {'partner': partner, 'form': form}));
    
@permission_required('partners.change_partner')
def partner_edit_telephone(request, id, telephone_id):
    """Edit a telephone number of the partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    telephone = get_object_or_404(Telephone, pk=telephone_id)
    if telephone.partner_set.get(id=partner.pk) is None:
        raise Http404
    
    if request.method == 'POST':
        form = PartnerTelephoneForm(request.POST, instance=telephone)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=partner.get_telephones_url())
    else:
        form = PartnerTelephoneForm(instance=telephone)

    return render_to_response('partners/edit_telephone.html', RequestContext(request, {'partner': partner, 'telephone': telephone, 'form': form}));
    
@permission_required('partners.change_partner')    
def partner_delete_telephone(request, id, telephone_id):
    """Delete a partner's telephone number.
    """
    partner = get_object_or_404(Partner, pk=id)
    telephone = get_object_or_404(Telephone, pk=telephone_id)
    if telephone.partner_set.get(id=partner.pk) is None:
        raise Http404

    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            telephone.delete()
        return redirect_to(request, url=partner.get_telephones_url())
    return render_to_response('partners/delete_telephone.html', RequestContext(request, {'partner': partner, 'telephone': telephone})) 
    
@permission_required('partners.change_partner')
def partner_add_address(request, id):
    """Add a new address for the partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    
    if request.method == 'POST':
        form = PartnerAddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            partner.addresses.add(address)
            return redirect_to(request, url=partner.get_addresses_url())
    else:
        form = PartnerAddressForm()

    return render_to_response('partners/add_address.html', RequestContext(request, {'partner': partner, 'form': form}));
    
@permission_required('partners.change_partner')
def partner_edit_address(request, id, address_id):
    """Edit a address of the partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    address = get_object_or_404(Address, pk=address_id)
    if address.partner_set.get(id=partner.pk) is None:
        raise Http404
    
    if request.method == 'POST':
        form = PartnerAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=partner.get_addresses_url())
    else:
        form = PartnerAddressForm(instance=address)

    return render_to_response('partners/edit_address.html', RequestContext(request, {'partner': partner, 'address': address, 'form': form}));
    
@permission_required('partners.change_partner')    
def partner_delete_address(request, id, address_id):
    """Delete a partner's address.
    """
    partner = get_object_or_404(Partner, pk=id)
    address = get_object_or_404(Address, pk=address_id)
    if address.partner_set.get(id=partner.pk) is None:
        raise Http404

    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            address.delete()
        return redirect_to(request, url=partner.get_addresses_url())
    return render_to_response('partners/delete_address.html', RequestContext(request, {'partner': partner, 'address': address})) 
    
@permission_required('partners.change_partner')
def partner_add_contact(request, id):
    """Add a new contact for the partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    job = Job(partner=partner)
    
    if request.method == 'POST':
        form = PartnerJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=partner.get_contacts_url())
    else:
        form = PartnerJobForm(instance=job)

    return render_to_response('partners/add_contact.html', RequestContext(request, {'partner': partner, 'form': form}));
    
@permission_required('partners.change_partner')
def partner_edit_contact(request, id, job_id):
    """Edit a contact of the partner.
    """
    partner = get_object_or_404(Partner, pk=id)
    job = get_object_or_404(Job, pk=job_id)
    if job.partner != partner:
        raise Http404
    
    if request.method == 'POST':
        form = PartnerJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=partner.get_contacts_url())
    else:
        form = PartnerJobForm(instance=job)

    return render_to_response('partners/edit_contact.html', RequestContext(request, {'partner': partner, 'job': job, 'form': form}));
    
@permission_required('partners.change_partner')    
def partner_delete_contact(request, id, job_id):
    """Delete a partner's contact.
    """
    partner = get_object_or_404(Partner, pk=id)
    job = get_object_or_404(Job, pk=job_id)
    if job.partner != partner:
        raise Http404

    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            job.delete()
        return redirect_to(request, url=partner.get_contacts_url())
    return render_to_response('partners/delete_contact.html', RequestContext(request, {'partner': partner, 'job': job}))

@permission_required('partners.change_contact')
def contact_index(request):
    """Show a contact list.
    """
    contacts = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        contacts = Contact.objects.filter(queryset)
    else:
        contacts = Contact.objects.all()
        
    contacts = ModelPaginatedListDetails(request, contacts)
        
    return render_to_response('partners/contacts/index.html', RequestContext(request, {'contacts': contacts}))

@permission_required('partners.add_contact')     
def contact_add(request):
    """Add a new contact.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect_to(request, url=contact.get_absolute_url())
    else:
        form = ContactForm()

    return render_to_response('partners/contacts/add.html', RequestContext(request, {'form': form}));

@permission_required('partners.change_contact')     
def contact_view(request, id, page=None):
    """Show contact details.
    """
    contact = get_object_or_404(Contact, pk=id)
    
    # Jobs.
    if page == 'jobs':
        jobs = PartnerJobListDetails(request, contact.job_set.select_related())
        return render_to_response('partners/contacts/jobs.html', RequestContext(request, {'contact': contact, 'jobs': jobs}))
    
    # Details.
    details = ContactDetails(instance=contact)
    return render_to_response('partners/contacts/view.html', RequestContext(request, {'contact': contact, 'details': details}))

@permission_required('partners.change_contact')     
def contact_edit(request, id):
    """Edit a contact.
    """
    contact = get_object_or_404(Contact, pk=id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=contact.get_absolute_url())
    else:
        form = ContactForm(instance=contact)
    return render_to_response('partners/contacts/edit.html', RequestContext(request, {'contact': contact, 'form': form}))

@permission_required('partners.delete_contact')    
def contact_delete(request, id):
    """Delete a contact.
    """
    contact = get_object_or_404(Contact, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            contact.delete()
            return redirect_to(request, url='/partners/contacts/');
        return redirect_to(request, url=contact.get_absolute_url())
    return render_to_response('partners/contacts/delete.html', RequestContext(request, {'contact': contact}))
    
@permission_required('partners.change_contact')
def contact_add_job(request, id):
    """Add a new job for the contact.
    """
    contact = get_object_or_404(Contact, pk=id)
    job = Job(contact=contact)
    
    if request.method == 'POST':
        form = ContactJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=contact.get_jobs_url())
    else:
        form = ContactJobForm(instance=job)

    return render_to_response('partners/contacts/add_job.html', RequestContext(request, {'contact': contact, 'form': form}));
    
@permission_required('partners.change_contact')
def contact_edit_job(request, id, job_id):
    """Edit a job of the contact.
    """
    contact = get_object_or_404(Contact, pk=id)
    job = get_object_or_404(Job, pk=job_id)
    if job.contact != contact:
        raise Http404
    
    if request.method == 'POST':
        form = ContactJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=contact.get_jobs_url())
    else:
        form = ContactJobForm(instance=job)

    return render_to_response('partners/contacts/edit_job.html', RequestContext(request, {'contact': contact, 'job': job, 'form': form}));
    
@permission_required('partners.change_contact')    
def contact_delete_job(request, id, job_id):
    """Delete a contact's job.
    """
    contact = get_object_or_404(Contact, pk=id)
    job = get_object_or_404(Job, pk=job_id)
    if job.contact != contact:
        raise Http404

    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            job.delete()
        return redirect_to(request, url=contact.get_jobs_url())
    return render_to_response('partners/contacts/delete_job.html', RequestContext(request, {'contact': contact, 'job': job}))
    
@permission_required('partners.change_role')
def role_index(request):
    """Show a role list.
    """
    roles = None
    queryset = None

    if request.method == 'POST' and request.POST.has_key(u'search'):
        token = request.POST['query']
        queryset = Q(name__startswith=token) | Q(name__endswith=token)

    if (queryset is not None):
        roles = Role.objects.filter(queryset)
    else:
        roles = Role.objects.all()
        
    roles = ModelPaginatedListDetails(request, roles)
        
    return render_to_response('partners/contacts/roles/index.html', RequestContext(request, {'roles': roles}))

@permission_required('partners.add_role')     
def role_add(request):
    """Add a new role.
    """
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            return redirect_to(request, url=role.get_absolute_url())
    else:
        form = RoleForm()

    return render_to_response('partners/contacts/roles/add.html', RequestContext(request, {'form': form}));

@permission_required('partners.change_role')     
def role_view(request, id, page=None):
    """Show role details.
    """
    role = get_object_or_404(Role, pk=id)
    details = ModelDetails(instance=role)
    return render_to_response('partners/contacts/roles/view.html', RequestContext(request, {'role': role, 'details': details}))

@permission_required('partners.change_role')     
def role_edit(request, id):
    """Edit a role.
    """
    role = get_object_or_404(Role, pk=id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect_to(request, url=role.get_absolute_url())
    else:
        form = RoleForm(instance=role)
    return render_to_response('partners/contacts/roles/edit.html', RequestContext(request, {'role': role, 'form': form}))

@permission_required('partners.delete_role')    
def role_delete(request, id):
    """Delete a role.
    """
    role = get_object_or_404(Role, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            role.delete()
            return redirect_to(request, url='/partners/contacts/roles/');
        return redirect_to(request, url=role.get_absolute_url())
    return render_to_response('partners/contacts/roles/delete.html', RequestContext(request, {'role': role}))
