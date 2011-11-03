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

urlpatterns = patterns('accounting.views',

    # Bank accounts.
    url(r'^bank-accounts/$', view='bankaccounts.bankaccount_list', name='bankaccount_list'),
    url(r'^bank-accounts/add/$', view='bankaccounts.bankaccount_add', name='bankaccount_add'),
    url(r'^bank-accounts/(?P<id>\d+)/$', view='bankaccounts.bankaccount_detail', name='bankaccount_detail'),
    url(r'^bank-accounts/(?P<id>\d+)/edit/$', view='bankaccounts.bankaccount_edit', name='bankaccount_edit'),
    url(r'^bank-accounts/(?P<id>\d+)/delete/$', view='bankaccounts.bankaccount_delete', name='bankaccount_delete'),

    # Sales invoices.
    url(r'^sales-invoices/$', view='salesinvoices.salesinvoice_list', name='salesinvoice_list'),
    url(r'^sales-invoices/add$', view='salesinvoices.salesinvoice_add', name='salesinvoice_add'),
    url(r'^sales-invoices/(?P<id>\d+)/$', view='salesinvoices.salesinvoice_detail', name='salesinvoice_detail'),
    url(r'^sales-invoices/(?P<id>\d+)/edit/$', view='salesinvoices.salesinvoice_edit', name='salesinvoice_edit'),
    url(r'^sales-invoices/(?P<id>\d+)/delete/$', view='salesinvoices.salesinvoice_delete', name='salesinvoice_delete'),
    url(r'^sales-invoices/(?P<id>\d+)/hard-copies/$', view='salesinvoices.salesinvoice_hardcopies', name='salesinvoice_hardcopies'),
    url(r'^sales-invoices/(?P<id>\d+)/hard-copies/add/$', view='salesinvoices.salesinvoice_add_hardcopy', name='salesinvoice_add_hardcopy'),
    url(r'^sales-invoices/(?P<id>\d+)/timeline/$', 'salesinvoices.salesinvoice_detail', {'template_name': 'accounting/salesinvoice_timeline.html'}, 'salesinvoice_timeline')
)
