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

from django import forms

from models import *

class SubscriptionsForm(forms.Form):
    """Form for notification subscriptions.
    """
    def __init__(self, *args, **kwargs):
        try:
            self.user = kwargs.pop('user')
        except KeyError:
            self.user = None
        super(SubscriptionsForm, self).__init__(*args, **kwargs)
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            name = subscription.signature
            field = forms.BooleanField(required=False, label=subscription.title, initial=(self.user in subscription.subscribers.all()))
            self.fields[name] = field
            
    def save(self):
        data = self.cleaned_data
        for key, value in data.iteritems():
            subscription = Subscription.objects.get(signature=key)
            if value and self.user not in subscription.subscribers.all():
                subscription.subscribers.add(self.user)
            elif not value and self.user in subscription.subscribers.all():
                subscription.subscribers.remove(self.user)
            subscription.save()
            
