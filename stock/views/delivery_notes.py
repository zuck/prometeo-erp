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
from django.contrib.contenttypes.models import ContentType

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.documents.models import Document
from prometeo.documents.forms import DocumentForm
from prometeo.products.forms import ProductEntryFormset

from ..models import *
from ..forms import *

def _get_delivery_note(request, *args, **kwargs):
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(DeliveryNote, id=id)
    return None

@permission_required('stock.change_delivery_note')
def delivery_note_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a delivery note list.
    """
    return filtered_list_detail(
        request,
        Document.objects.filter(content_type=ContentType.objects.get_for_model(DeliveryNote)),
        fields=['code', 'author', 'created'],
        page=page,
        paginate_by=paginate_by,
        template_name='stock/delivery_note_list.html',
        **kwargs
    )

@permission_required('stock.add_delivery_note')     
def delivery_note_add(request, **kwargs):
    """Adds a new delivery note.
    """
    delivery_note = DeliveryNote()
    doc = Document(author=request.user)
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = DeliveryNoteForm(request.POST, instance=delivery_note)
        formset = ProductEntryFormset(request.POST)
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            doc.content_object = delivery_note 
            dform.save()
            for e in formset.save():
                delivery_note.entries.add(e)
            messages.success(request, _("The delivery note has been saved."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = DeliveryNoteForm(instance=delivery_note)
        formset = ProductEntryFormset()

    return render_to_response('stock/delivery_note_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('stock.change_delivery_note', _get_delivery_note)     
def delivery_note_detail(request, id, page=None, **kwargs):
    """Shows delivery note details.
    """
    object_list = Document.objects.filter(content_type=ContentType.objects.get_for_model(DeliveryNote))

    return list_detail.object_detail(
        request,
        object_id=Document.objects.get(object_id=id).pk,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        template_name='stock/delivery_note_detail.html',
        **kwargs
    )

@permission_required('stock.change_delivery_note', _get_delivery_note)     
def delivery_note_edit(request, id, **kwargs):
    """Edits a delivery note.
    """
    doc = get_object_or_404(Document, content_type=ContentType.objects.get_for_model(DeliveryNote), object_id=id)
    delivery_note = doc.content_object
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = DeliveryNoteForm(request.POST, instance=delivery_note)
        formset = ProductEntryFormset(request.POST, queryset=delivery_note.entries.all())
        if form.is_valid() and dform.is_valid() and formset.is_valid():
            form.save()
            dform.save()
            for e in formset.save():
                delivery_note.entries.add(e)
            messages.success(request, _("The delivery note has been saved."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = DeliveryNoteForm(instance=delivery_note)
        formset = ProductEntryFormset(queryset=delivery_note.entries.all())

    return render_to_response('stock/delivery_note_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'formset': formset, 'object': doc}))

@permission_required('stock.delete_delivery_note', _get_delivery_note)    
def delivery_note_delete(request, id, **kwargs):
    """Deletes a delivery note.
    """
    return create_update.delete_object(
        request,
        model=DeliveryNote,
        object_id=id,
        post_delete_redirect=reverse('delivery_note_list'),
        template_name='stock/delivery_note_delete.html',
        **kwargs
    )
