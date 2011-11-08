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

from cStringIO import StringIO

from xhtml2pdf import pisa

from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse

def render_to_pdf(request, template_name, context, filename="report.pdf", encoding='utf-8', **kwargs):
    """Renders a pdf response using given *request*, *template_name* and *context*.
    """
    if not isinstance(context, Context):
        context = RequestContext(request, context)

    content = render_to_string(template_name, context)
    src = StringIO(content.encode(encoding))
    out = StringIO()
    result = pisa.CreatePDF(src, out, **kwargs)

    if not result.err:
        response = HttpResponse(out.getvalue(), mimetype='application/pdf')
        if filename is not None:
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    return ""
