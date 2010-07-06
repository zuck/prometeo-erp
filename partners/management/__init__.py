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

__author__ = 'Emanuele Bertoldi <zuck@fastwebnet.it>'
__copyright__ = 'Copyright (c) 2010 Emanuele Bertoldi'
__version__ = '$Revision$'

from django.db.models import get_models, signals
from prometeo.partners import models as partner_app

def create_managed_partner(app, created_models, verbosity, **kwargs):
    from prometeo.partners.models import Partner
    if Partner in created_models and kwargs.get('interactive', True):
        msg = "\nYou just installed Prometeo's partners system, which means you don't have " \
                "a default managed company defined.\nWould you like to create one now? (yes/no): "
        confirm = raw_input(msg)
        while 1:
            if confirm not in ('yes', 'no'):
                confirm = raw_input('Please enter either "yes" or "no": ')
                continue
            if confirm == 'yes':
                name = raw_input("Insert the company's name: ")
                vat = raw_input("Insert the VAT number (optional): ")
                email = raw_input("Insert the main email address (optional): ")
                url = raw_input("Insert the main URL address (optional): ")
                notes = raw_input("Insert additional notes (optional): ")
                if Partner.objects.create(name=name, vat_number=vat, email=email, url=url, notes=notes, is_managed=True):
                    print "Default managed company created successfully.\n"
            break

signals.post_syncdb.connect(create_managed_partner,
    sender=partner_app, dispatch_uid = "prometeo.partners.management.create_managed_partner")
