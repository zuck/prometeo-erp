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
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import list_detail, create_update

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from ..models import *
from ..forms import *

def _get_bankaccount(request, *args, **kwargs):
    bankaccount_id = kwargs.get('bankaccount_id', None)
    id = kwargs.get('id', None)
    if bankaccount_id:
        return get_object_or_404(BankAccount, id=bankaccount_id)
    elif id:
        return get_object_or_404(BankAccount, id=id)
    return None

@permission_required('sales.view_bankaccount')
def bankaccount_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a bank account list.
    """
    return filtered_list_detail(
        request,
        BankAccount,
        fields=['bank_name', 'bic', 'iban', 'owner'],
        page=page,
        paginate_by=paginate_by,
        template_name='sales/bankaccount_list.html',
        **kwargs
    )

@permission_required('sales.add_bankaccount')     
def bankaccount_add(request, **kwargs):
    """Adds a new bank account.
    """
    return create_update.create_object(
        request,
        form_class=BankAccountForm,
        template_name='sales/bankaccount_edit.html'
    )

@permission_required('sales.view_bankaccount', _get_bankaccount)     
def bankaccount_detail(request, id, page=None, **kwargs):
    """Shows bank account details.
    """
    object_list = BankAccount.objects.all()

    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        template_name='sales/bankaccount_detail.html',
        **kwargs
    )

@permission_required('sales.change_bankaccount', _get_bankaccount)     
def bankaccount_edit(request, id, **kwargs):
    """Edits a bank account.
    """
    return create_update.update_object(
        request,
        object_id=id,
        form_class=BankAccountForm,
        template_name='sales/bankaccount_edit.html'
    )

@permission_required('sales.delete_bankaccount', _get_bankaccount)    
def bankaccount_delete(request, id, **kwargs):
    """Deletes a bank account.
    """
    return create_update.delete_object(
        request,
        model=BankAccount,
        object_id=id,
        post_delete_redirect=reverse('bankaccount_list'),
        template_name='sales/bankaccount_delete.html',
        **kwargs
    )
