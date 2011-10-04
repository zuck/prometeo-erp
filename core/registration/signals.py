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

import datetime, random, hashlib

from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings

from prometeo.core.auth.models import UserProfile

from models import *

def user_profile_post_save(sender, instance, signal, *args, **kwargs):
    if kwargs['created'] and UserProfile.objects.count() > 1:
        token, is_new = ActivationToken.objects.get_or_create(profile=instance)
        if not is_new:
            return

        # Creates an activation key.
        sha = hashlib.sha1()
        sha.update(str(random.random()))
        sha.update(instance.user.username)
        token.activation_key = sha.hexdigest()
        token.key_expiration = datetime.datetime.today() + datetime.timedelta(settings.AUTH_EXPIRATION_DAYS)
        token.save()
        
        # Updates the user activation status.
        instance.user.is_active = False
        instance.user.save()
        
        # Send an activation email.
        current_site = Site.objects.get_current()
        activation_url = 'http://' + current_site.domain + reverse('user_activate', args=[token.activation_key])
        email_subject = 'Account confirmation'
        email_body = u'<p>Hello <strong>%s</strong>, and thanks for signing up for an account on <strong>%s</strong>.</p>' \
                     u'<p>To activate your account, click this link within <strong>%s day(s)</strong>:</p>' \
                     u'<p><a href="%s">%s</a></p>' % (instance.user.username, current_site.name, settings.AUTH_EXPIRATION_DAYS, activation_url, activation_url)
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
        email = EmailMessage(email_subject, email_body, email_from, [instance.user.email,])
        email.content_subtype = "html"
        email.send()

models.signals.post_save.connect(user_profile_post_save, UserProfile)
