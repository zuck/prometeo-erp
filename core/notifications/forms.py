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

from django import forms
from django.utils.translation import ugettext_lazy as _

from prometeo.core.forms import enrich_form

from models import *

class SubscriptionWidget(forms.MultiWidget):
    """Widget for subscription entry.
    """
    def __init__(self, *args, **kwargs):
        kwargs['widgets'] = (
            forms.CheckboxInput(attrs={'class': 'subscribe'}),
            forms.CheckboxInput(attrs={'class': 'email'})
        )
        super(SubscriptionWidget, self).__init__(*args, **kwargs)

    def decompress(self, value):
        if value:
            return value.values()
        return (False, False)

    def format_output(self, rendered_widgets):
        return '<td>%s</td>' % '</td>\n<td>'.join(rendered_widgets)

class SubscriptionField(forms.MultiValueField):
    """Field for subscription entry.
    """
    widget = SubscriptionWidget

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {'subscribe': False, 'email': False}
        initial = kwargs['initial']
        kwargs['fields'] = (
            forms.BooleanField(required=False, label=_('subscribe'), initial=initial['subscribe']),
            forms.BooleanField(required=False, label=_('send email'), initial=initial['email'])
        )
        super(SubscriptionField, self).__init__(*args, **kwargs)

    def compress(self, data_list):
        if len(data_list) >= 2:
            return (data_list[0], data_list[1])
        return None

class SubscriptionsForm(forms.Form):
    """Form for notification subscriptions.
    """
    def __init__(self, *args, **kwargs):
        try:
            self.user = kwargs.pop('user')
        except KeyError:
            self.user = None
        super(SubscriptionsForm, self).__init__(*args, **kwargs)
        signatures = Signature.objects.all()
        for signature in signatures:
            name = signature.slug
            is_subscriber = (Subscription.objects.filter(signature=signature, user=self.user).count() > 0)
            send_email = (Subscription.objects.filter(signature=signature, user=self.user, send_email=True).count() > 0)
            field = SubscriptionField(label=signature.title, initial={'subscribe': is_subscriber, 'email': send_email})
            self.fields[name] = field
            
    def save(self):
        data = self.cleaned_data
        for key, (subscribe, email) in data.iteritems():
            signature = Signature.objects.get(slug=key)
            is_subscriber = (self.user in signature.subscribers.all())
            if subscribe:
                subscription = Subscription.objects.get_or_create(user=self.user, signature=signature)[0]
                subscription.send_email = email
                subscription.save()
            elif is_subscriber and not subscribe:
                Subscription.objects.filter(user=self.user, signature=signature).delete()
                self.fields[key].initial = (False, False)
                 
enrich_form(SubscriptionsForm)
