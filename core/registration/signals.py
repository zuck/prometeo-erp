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

import datetime, random, hashlib

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from prometeo.core.auth.models import UserProfile

from models import *

def user_profile_post_save(sender, instance, signal, *args, **kwargs):
    if kwargs['created'] \
    and not instance.user.is_active \
    and UserProfile.objects.count() > 1:        
        token, is_new = ActivationToken.objects.get_or_create(profile=instance)
        if is_new:
            # Creates an activation key.
            sha = hashlib.sha1()
            sha.update(str(random.random()))
            sha.update(instance.user.username)
            token.activation_key = sha.hexdigest()
            token.key_expiration = datetime.datetime.today() + datetime.timedelta(settings.AUTH_EXPIRATION_DAYS)
            token.save()
            
            # Send an activation email.
            current_site = Site.objects.get_current()
            activation_link = 'http://' + current_site.domain + reverse('user_activate', args=[token.activation_key])
            context = {
                "user_name": instance.user.username,
                "current_site": current_site.name,
                "expiration_time": settings.AUTH_EXPIRATION_DAYS,
                "activation_link": activation_link
            }
            email_subject = _('Account confirmation')
            email_body = render_to_string("registration/emails/activation.html", context)
            email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
            email = EmailMessage(email_subject, email_body, email_from, [instance.user.email,])
            email.content_subtype = "html"
            email.send()

models.signals.post_save.connect(user_profile_post_save, UserProfile)
