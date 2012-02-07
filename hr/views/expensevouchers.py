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

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.documents.models import *
from prometeo.documents.forms import *
from prometeo.documents.views import *

from ..forms import *

def _get_expensevoucher(request, *args, **kwargs):
    return get_object_or_404(ExpenseVoucher, id=kwargs.get('id', None))

def _get_expenseentry(request, *args, **kwargs):
    return get_object_or_404(ExpenseEntry, voucher__id=kwargs.get('voucher_id', None), id=kwargs.get('id', None))

@permission_required('hr.view_expensevoucher') 
def expensevoucher_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered expensevouchers.
    """
    return filtered_list_detail(
        request,
        Document.objects.get_for_content(ExpenseVoucher),
        fields=['code', 'author', 'created', 'owner', 'status'],
        paginate_by=paginate_by,
        page=page,
        template_name='hr/expensevoucher_list.html',
        **kwargs
    )

@permission_required('hr.view_expensevoucher', _get_expensevoucher)  
def expensevoucher_detail(request, id, **kwargs):
    """Displays a expensevoucher.
    """
    object_list = Document.objects.get_for_content(ExpenseVoucher)
    return list_detail.object_detail(
        request,
        object_id=object_list.get(object_id=id).pk,
        queryset=object_list,
        template_name=kwargs.pop('template_name', 'hr/expensevoucher_detail.html'),
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('hr.add_expensevoucher')    
def expensevoucher_add(request, **kwargs):
    """Adds a new expensevoucher.
    """
    expensevoucher = ExpenseVoucher(date=datetime.now().date())  
    doc = Document(author=request.user, content_object=expensevoucher)
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = ExpenseVoucherForm(request.POST, instance=expensevoucher)
        formset = ExpenseEntryFormset(request.POST, instance=expensevoucher)
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            doc.content_object = expensevoucher
            dform.save()
            formset.save()
            messages.success(request, _("The expense voucher was created successfully."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = ExpenseVoucherForm(instance=expensevoucher)
        formset = ExpenseEntryFormset(instance=expensevoucher)

    return render_to_response('hr/expensevoucher_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('hr.change_expensevoucher', _get_expensevoucher)  
def expensevoucher_edit(request, id, **kwargs):
    """Edits a expensevoucher.
    """
    doc = Document.objects.get_for_content(ExpenseVoucher).get(object_id=id)
    expensevoucher = doc.content_object
        
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = ExpenseVoucherForm(request.POST, instance=expensevoucher)
        formset = ExpenseEntryFormset(request.POST, instance=expensevoucher)
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            dform.save()
            formset.save()
            messages.success(request, _("The expense voucher was updated successfully."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = ExpenseVoucherForm(instance=expensevoucher)
        formset = ExpenseEntryFormset(instance=expensevoucher)

    return render_to_response('hr/expensevoucher_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('hr.delete_expensevoucher', _get_expensevoucher) 
def expensevoucher_delete(request, id, **kwargs):
    """Deletes a expensevoucher.
    """
    return create_update.delete_object(
            request,
            model=Document,
            object_id=Document.objects.get_for_content(ExpenseVoucher).get(object_id=id).pk,
            post_delete_redirect=reverse('expensevoucher_list'),
            template_name='hr/expensevoucher_delete.html',
            **kwargs
        )

@permission_required('hr.view_expensevoucher', _get_expensevoucher)     
def expensevoucher_hardcopies(request, id, page=0, paginate_by=10, **kwargs):
    """Shows expensevoucher hard copies.
    """
    return hardcopy_list(request, Document.objects.get_for_content(ExpenseVoucher).get(object_id=id).pk, page, paginate_by, **kwargs)

@permission_required('hr.change_expensevoucher', _get_expensevoucher)     
def expensevoucher_add_hardcopy(request, id, **kwargs):
    """Adds an hard copy to the given document.
    """
    return hardcopy_add(request, Document.objects.get_for_content(ExpenseVoucher).get(object_id=id).pk, **kwargs)

@permission_required('hr.change_expenseentry', _get_expenseentry)
def expenseentry_delete(request, voucher_id, id, **kwargs):
    """Deletes a expensevoucher entry.
    """
    return create_update.delete_object(
            request,
            model=ExpenseEntry,
            object_id=id,
            post_delete_redirect=expensevoucher.get_absolute_url(),
            template_name='hr/expenseentry_delete.html',
            **kwargs
        )
