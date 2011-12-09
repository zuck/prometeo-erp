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
from prometeo.documents.models import *
from prometeo.documents.forms import *
from prometeo.documents.views import *
from prometeo.products.forms import ProductEntryFormset

from ..models import *
from ..forms import *

def _get_letter(request, *args, **kwargs):
    note_id = kwargs.get('note_id', None)
    if note_id:
        return get_object_or_404(Letter, id=note_id)
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(Letter, id=id)
    return None

@permission_required('partners.change_letter')
def letter_list(request, page=0, paginate_by=10, **kwargs):
    """Shows a letter list.
    """
    return filtered_list_detail(
        request,
        Document.objects.get_for_content(Letter),
        fields=['code', 'author', 'created', 'owner'],
        page=page,
        paginate_by=paginate_by,
        template_name='partners/letter_list.html',
        **kwargs
    )

@permission_required('partners.add_letter')     
def letter_add(request, **kwargs):
    """Adds a new letter.
    """
    letter = Letter()
    doc = Document(author=request.user, content_object=letter)
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = LetterForm(request.POST, instance=letter)
        if form.is_valid() and dform.is_valid():
            form.save()
            doc.content_object = letter 
            dform.save()
            messages.success(request, _("The letter has been saved."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = LetterForm(instance=letter)

    return render_to_response('partners/letter_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'object': doc}))

@permission_required('partners.change_letter', _get_letter)     
def letter_detail(request, id, page=None, **kwargs):
    """Shows letter details.
    """
    object_list = Document.objects.get_for_content(Letter)

    return list_detail.object_detail(
        request,
        object_id=object_list.get(object_id=id).pk,
        queryset=object_list,
        extra_context={
            'object_list': object_list,
        },
        template_name=kwargs.pop('template_name', 'partners/letter_detail.html'),
        **kwargs
    )

@permission_required('partners.change_letter', _get_letter)     
def letter_edit(request, id, **kwargs):
    """Edits a letter.
    """
    doc = get_object_or_404(Document.objects.get_for_content(Letter), object_id=id)
    letter = doc.content_object
      
    if request.method == 'POST':
        dform = DocumentForm(request.POST, instance=doc)
        form = LetterForm(request.POST, instance=letter)
        if form.is_valid() and dform.is_valid():
            form.save()
            dform.save()
            messages.success(request, _("The letter has been updated."))
            return redirect_to(request, url=doc.get_absolute_url())
    else:
        dform = DocumentForm(instance=doc)
        form = LetterForm(instance=letter)

    return render_to_response('partners/letter_edit.html', RequestContext(request, {'form': form, 'dform': dform, 'object': doc}))

@permission_required('partners.delete_letter', _get_letter)    
def letter_delete(request, id, **kwargs):
    """Deletes a letter.
    """
    return create_update.delete_object(
        request,
        model=Document,
        object_id=Document.objects.get_for_content(Letter).get(object_id=id).pk,
        post_delete_redirect=reverse('letter_list'),
        template_name='partners/letter_delete.html',
        **kwargs
    )

@permission_required('partners.change_letter', _get_letter)     
def letter_hardcopies(request, id, page=0, paginate_by=10, **kwargs):
    """Shows letter hard copies.
    """
    return hardcopy_list(request, Document.objects.get_for_content(Letter).get(object_id=id).pk, page, paginate_by, **kwargs)

@permission_required('partners.change_letter', _get_letter)     
def letter_add_hardcopy(request, id, **kwargs):
    """Adds an hard copy to the given document.
    """
    return hardcopy_add(request, Document.objects.get_for_content(Letter).get(object_id=id).pk, **kwargs)
