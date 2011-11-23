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

from django.utils.translation import ugettext_lazy as _

MEANS_OF_DELIVERY = (
    ('SENDER', _('sender')),
    ('ADDRESSEE', _('addressee')),
    ('CARRIER', _('carrier')),
)

DEFAULT_MEAN_OF_DELIVERY = 'CARRIER'

TERMS_OF_SHIPPING = (
    ('EXW', _('EXW')),
    ('FCA', _('FCA')),
    ('CPT', _('CPT')),
    ('CIP', _('CIP')),
    ('DAT', _('DAT')),
    ('DAP', _('DAP')),
    ('DDP', _('DDP')),
    ('FAS', _('FAS')),
    ('FOB', _('FOB')),
    ('CFR', _('CFR')),
    ('CIF', _('CIF')),
)

DEFAULT_TERMS_OF_SHIPPING = 'CPT'

GOODS_APPEARANCES = (
    ('BOX', _('box')),
)

DEFAULT_GOODS_APPEARANCE = 'BOX'
