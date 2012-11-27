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

from django.conf.urls.defaults import *

urlpatterns = patterns('partners.views',

    # Partners.
    url(r'^partners/$', view='partners.partner_list', name='partner_list'),
    url(r'^partners/add/$', view='partners.partner_add', name='partner_add'),
    url(r'^partners/(?P<id>\d+)/$', view='partners.partner_detail', name='partner_detail'),
    url(r'^partners/(?P<id>\d+)/edit/$', view='partners.partner_edit', name='partner_edit'),
    url(r'^partners/(?P<id>\d+)/delete/$', view='partners.partner_delete', name='partner_delete'),
    url(r'^partners/(?P<id>\d+)/addresses/$', view='partners.partner_addresses', name='partner_addresses'),
    url(r'^partners/(?P<id>\d+)/addresses/add/$', view='partners.partner_add_address', name='partner_add_address'),
    url(r'^partners/(?P<partner_id>\d+)/addresses/(?P<id>\d+)/edit/$', view='partners.partner_edit_address', name='partner_edit_address'),
    url(r'^partners/(?P<partner_id>\d+)/addresses/(?P<id>\d+)/delete/$', view='partners.partner_delete_address', name='partner_delete_address'),
    url(r'^partners/(?P<id>\d+)/phones/$', view='partners.partner_phones', name='partner_phones'),
    url(r'^partners/(?P<id>\d+)/phones/add/$', view='partners.partner_add_phone', name='partner_add_phone'),
    url(r'^partners/(?P<partner_id>\d+)/phones/(?P<id>\d+)/edit/$', view='partners.partner_edit_phone', name='partner_edit_phone'),
    url(r'^partners/(?P<partner_id>\d+)/phones/(?P<id>\d+)/delete/$', view='partners.partner_delete_phone', name='partner_delete_phone'),
    url(r'^partners/(?P<id>\d+)/profiles/$', view='partners.partner_profiles', name='partner_profiles'),
    url(r'^partners/(?P<id>\d+)/profiles/add/$', view='partners.partner_add_profile', name='partner_add_profile'),
    url(r'^partners/(?P<partner_id>\d+)/profiles/(?P<id>\d+)/edit/$', view='partners.partner_edit_profile', name='partner_edit_profile'),
    url(r'^partners/(?P<partner_id>\d+)/profiles/(?P<id>\d+)/delete/$', view='partners.partner_delete_profile', name='partner_delete_profile'),
    url(r'^partners/(?P<id>\d+)/contacts/$', view='partners.partner_contacts', name='partner_contacts'),
    url(r'^partners/(?P<id>\d+)/contacts/add/$', view='partners.partner_add_contact', name='partner_add_contact'),
    url(r'^partners/(?P<id>\d+)/communications/$', view='partners.partner_communications', name='partner_communications'),
    url(r'^partners/(?P<id>\d+)/communications/add/$', view='partners.partner_add_communication', name='partner_add_communication'),
    url(r'^partners/(?P<id>\d+)/timeline/$', 'partners.partner_detail', {"template_name": "partners/partner_timeline.html"}, 'partner_timeline'),

    # Contacts.
    url(r'^contacts/$', view='contacts.contact_list', name='contact_list'),
    url(r'^contacts/add/$', view='contacts.contact_add', name='contact_add'),
    url(r'^contacts/(?P<id>\d+)/$', view='contacts.contact_detail', name='contact_detail'),
    url(r'^contacts/(?P<id>\d+)/edit/$', view='contacts.contact_edit', name='contact_edit'),
    url(r'^contacts/(?P<id>\d+)/delete/$', view='contacts.contact_delete', name='contact_delete'),
    url(r'^contacts/(?P<id>\d+)/addresses/$', view='contacts.contact_addresses', name='contact_addresses'),
    url(r'^contacts/(?P<id>\d+)/addresses/add/$', view='contacts.contact_add_address', name='contact_add_address'),
    url(r'^contacts/(?P<contact_id>\d+)/addresses/(?P<id>\d+)/edit/$', view='contacts.contact_edit_address', name='contact_edit_address'),
    url(r'^contacts/(?P<contact_id>\d+)/addresses/(?P<id>\d+)/delete/$', view='contacts.contact_delete_address', name='contact_delete_address'),
    url(r'^contacts/(?P<id>\d+)/phones/$', view='contacts.contact_phones', name='contact_phones'),
    url(r'^contacts/(?P<id>\d+)/phones/add/$', view='contacts.contact_add_phone', name='contact_add_phone'),
    url(r'^contacts/(?P<contact_id>\d+)/phones/(?P<id>\d+)/edit/$', view='contacts.contact_edit_phone', name='contact_edit_phone'),
    url(r'^contacts/(?P<contact_id>\d+)/phones/(?P<id>\d+)/delete/$', view='contacts.contact_delete_phone', name='contact_delete_phone'),
    url(r'^contacts/(?P<id>\d+)/profiles/$', view='contacts.contact_profiles', name='contact_profiles'),
    url(r'^contacts/(?P<id>\d+)/profiles/add/$', view='contacts.contact_add_profile', name='contact_add_profile'),
    url(r'^contacts/(?P<contact_id>\d+)/profiles/(?P<id>\d+)/edit/$', view='contacts.contact_edit_profile', name='contact_edit_profile'),
    url(r'^contacts/(?P<contact_id>\d+)/profiles/(?P<id>\d+)/delete/$', view='contacts.contact_delete_profile', name='contact_delete_profile'),
    url(r'^contacts/(?P<id>\d+)/jobs/$', view='contacts.contact_jobs', name='contact_jobs'),
    url(r'^contacts/(?P<id>\d+)/jobs/add/$', view='contacts.contact_add_job', name='contact_add_job'),
    url(r'^contacts/(?P<contact_id>\d+)/jobs/(?P<id>\d+)/edit/$', view='contacts.contact_edit_job', name='contact_edit_job'),
    url(r'^contacts/(?P<contact_id>\d+)/jobs/(?P<id>\d+)/delete/$', view='contacts.contact_delete_job', name='contact_delete_job'),
    url(r'^contacts/(?P<id>\d+)/timeline/$', 'contacts.contact_detail', {"template_name": "partners/contact_timeline.html"}, 'contact_timeline'),

    # Communications.
    url(r'^communications/$', view='communications.communication_list', name='communication_list'),
    url(r'^communications/add/$', view='communications.communication_add', name='communication_add'),
    url(r'^communications/(?P<id>\d+)/$', view='communications.communication_detail', name='communication_detail'),
    url(r'^communications/(?P<id>\d+)/edit/$', view='communications.communication_edit', name='communication_edit'),
    url(r'^communications/(?P<id>\d+)/delete/$', view='communications.communication_delete', name='communication_delete'),
    url(r'^communications/(?P<id>\d+)/hardcopies/$', view='communications.communication_hardcopies', name='communication_hardcopies'),
    url(r'^communications/(?P<id>\d+)/hardcopies/add/$', view='communications.communication_add_hardcopy', name='communication_add_hardcopy'),
    url(r'^communications/(?P<id>\d+)/timeline/$', 'communications.communication_detail', {'template_name': 'partners/communication_timeline.html'}, 'communication_timeline'),
)
