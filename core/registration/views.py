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

import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from models import *
from forms import *

def user_register(request):
    """Registers a new user account.
    """
    if request.user.is_authenticated():
        messages.info(request, _("You are already registered."))
        return redirect_to(request, url="/")
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _("An email has been sent with an activation key. Please check your mail to complete the registration."))
            return redirect_to(request, url="/")
    else:
        form = UserRegistrationForm()

    return render_to_response('registration/register.html', RequestContext(request, {'form': form}))        
    
def user_activate(request, activation_key):
    """Activates a pending user account.
    """
    token = get_object_or_404(ActivationToken, activation_key=activation_key)
    user_account = token.profile.user
    if user_account.is_active:
        messages.info(request, _("This account is already active."))
        if request.user.is_authenticated():
            return redirect_to(request, url="/")
        return redirect_to(request, reverse('user_login'))
    try:
        if token.key_expiration < datetime.datetime.today():
            messages.error(request, _("Sorry, your account is expired."))
            return redirect_to(request, url="/")
    except TypeError:
        pass
    user_account.is_active = True
    user_account.save()
    messages.success(request, _("Congratulations! Your account is now active."))
    return redirect_to(request, reverse('user_login'))
