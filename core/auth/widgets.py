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
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from forms import *

def contact_form(context):
    """Adds a contact form to the context.
    """
    request = context['request']
    initial = {}
    try:
        initial['email'] = request.user.email
    except AttributeError:
        pass
    form = ContactForm(initial=initial)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['email']
            to_email = getattr(settings, 'DEFAULT_TO_EMAIL', 'info@localhost.com')

            if (send_mail(subject, message, from_email, [to_email])):
                form = ContactForm(initial=initial) # Form reset.
                message = messages.success(request, 'Thank you. Your email has been sent.')
            else:
                message = messages.error(request, 'Sorry. An error has been occured. Please, try again.')
        
    context['contact_form'] = form
    return context
