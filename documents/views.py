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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import get_language, ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail, set_language
from prometeo.core.views.reports import render_to_pdf

from models import *
from forms import *

def _get_document(request, *args, **kwargs):
    document_id = kwargs.get('document_id', None)
    if document_id:
        return get_object_or_404(Document, id=document_id)
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(Document, id=id)
    return None

def document_print(request, id, lang=None, template_name=None, **kwargs):
    """Prints a document to a .pdf file.
    """
    old_lang = get_language()
    if lang:
        set_language(request, lang)
    doc = get_object_or_404(Document, id=id)
    filename = "%s.pdf" % doc.filename
    if not template_name:
        template_name = "%s/%s_pdf.html" % (doc.content_type.app_label, doc.content_type.model)
    response = render_to_pdf(request, template_name, {'document': doc}, filename, **kwargs)
    set_language(request, old_lang)
    return response

@permission_required('documents.view_document', _get_document) 
def hardcopy_list(request, id, page=0, paginate_by=10, **kwargs):
    """Displays the list of all hard copies of the given document.
    """
    document = get_object_or_404(Document, id=id)

    return filtered_list_detail(
        request,
        HardCopy.objects.filter(document=document),
        paginate_by=paginate_by,
        page=page,
        fields=['file', 'language', 'created'],
        extra_context={
            'object': document,
        },
        template_name=kwargs.pop('template_name', '%s/%s_hardcopies.html' % (document.content_type.app_label, document.content_type.model)),
        **kwargs
    )

@permission_required('documents.change_document', _get_document) 
def hardcopy_add(request, id, **kwargs):
    """Deletes a delivery note.
    """
    document = get_object_or_404(Document, id=id)
    hardcopy = HardCopy(document=document, author=request.user)

    template_name = kwargs.pop('template_name', '%s/%s_edit_hardcopy.html' % (document.content_type.app_label, document.content_type.model))
    post_add_redirect = kwargs.pop('post_add_redirect', reverse('%s_hardcopies' % document.content_type.model, args=[document.object_id]))
      
    if request.method == 'POST':
        form = HardCopyForm(request.POST, request.FILES, instance=hardcopy)
        if form.is_valid():
            form.save()
            messages.success(request, _("The hard copy has been saved."))
            return redirect_to(request, url=post_add_redirect)
    else:
        form = HardCopyForm(instance=hardcopy)

    return render_to_response(template_name, RequestContext(request, {'form': form, 'object': hardcopy}))

@permission_required('documents.change_document', _get_document) 
def hardcopy_delete(request, document_id, id, **kwargs):
    """Deletes a delivery note.
    """
    document = get_object_or_404(Document, id=document_id)

    return create_update.delete_object(
        request,
        model=HardCopy,
        object_id=id,
        post_delete_redirect=kwargs.pop('post_delete_redirect', reverse('%s_hardcopies' % document.content_type.model, args=[document.object_id])),
        template_name=kwargs.pop('template_name', '%s/%s_delete_hardcopy.html' % (document.content_type.app_label, document.content_type.model)),
        **kwargs
    )
