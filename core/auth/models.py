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

from pytz import common_timezones

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage

from prometeo.core.menus.signals import manage_bookmarks
from prometeo.core.widgets.signals import manage_dashboard

TIME_ZONES = [(tz, tz) for tz in common_timezones]
 
class UserProfile(models.Model):
    """User profile.
    """
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=5, null=True, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, verbose_name=_("language"))
    timezone = models.CharField(max_length=20, null=True, choices=TIME_ZONES, default=settings.TIME_ZONE, verbose_name=_("timezone"))
    dashboard = models.OneToOneField('widgets.Region', null=True, verbose_name=_("dashboard"))
    bookmarks = models.OneToOneField('menus.Menu', null=True, verbose_name=_("bookmarks"))

def user_post_save(sender, instance, signal, *args, **kwargs):
    profile, is_new = UserProfile.objects.get_or_create(user=instance)
    if is_new and UserProfile.objects.count() > 1:
        # Creates an activation key.
        sha = hashlib.sha1()
        sha.update(str(random.random()))
        sha.update(instance.username)
        profile.activation_key = sha.hexdigest()
        profile.key_expires = datetime.datetime.today() + datetime.timedelta(settings.AUTH_EXPIRATION_DAYS)
        profile.save()
        
        # Updates the user activation status.
        instance.is_active = False
        instance.save()
        
        # Send an activation email.
        current_site = Site.objects.get_current()
        activation_url = 'http://' + current_site.domain + reverse('user_activate', args=[profile.activation_key])
        email_subject = 'Account confirmation'
        email_body = u'<p>Hello <strong>%s</strong>, and thanks for signing up for an account on <strong>%s</strong>.</p>' \
                     u'<p>To activate your account, click this link within <strong>%s day(s)</strong>:</p>' \
                     u'<p><a href="%s">%s</a></p>' % (instance.username, current_site.name, settings.AUTH_EXPIRATION_DAYS, activation_url, activation_url)
        email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@localhost.com')
        email = EmailMessage(email_subject, email_body, email_from, [instance.email,])
        email.content_subtype = "html"
        email.send()

models.signals.post_save.connect(user_post_save, User)

manage_bookmarks(UserProfile)
manage_dashboard(UserProfile)

