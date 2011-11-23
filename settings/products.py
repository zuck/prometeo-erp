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

PRODUCT_UOM_CHOICES = (
    ('BG', _('Bag')),
    ('BR', _('Barrel')),
    ('BL', _('Block')),
    ('B8', _('Board')),
    ('BF', _('Board Feet')),
    ('BO', _('Bottle')),
    ('BX', _('Box')),
    ('BN', _('Bulk')),
    ('BD', _('Bundle')),
    ('CG', _('Card')),
    ('CT', _('Carton')),
    ('CQ', _('Cartridge')),
    ('CA', _('Case')),
    ('C3', _('Centigram')),
    ('CM', _('Centiliter')),
    ('1N', _('Count')),
    ('CC', _('Cubic Centimeter')),
    ('C8', _('Cubic Decimeter')),
    ('CF', _('Cubic Feet')),
    ('CI', _('Cubic Inches')),
    ('CR', _('Cubic Meter')),
    ('MMQ', _('Cubic Milimetre')),
    ('DA', _('Days')),
    ('DG', _('Decigram')),
    ('DL', _('Deciliter')),
    ('DM', _('Decimeter')),
    ('CE', _('Degrees Celsius')),
    ('FA', _('Degrees Fahrenheit')),
    ('DZ', _('Dozen')),
    ('FT', _('Feet')),
    ('UZ', _('Fifty Count')),
    ('UY', _('Fifty Square Feet')),
    ('FO', _('Fluid Ounce')),
    ('GA', _('Gallon')),
    ('GR', _('Gram')),
    ('GT', _('Gross Kilogram')),
    ('HD', _('Half Dozen')),
    ('HC', _('Houndred Count')),
    ('HL', _('Houndred Feet')),
    ('CW', _('Houndred Pounds')),
    ('IN', _('Inches')),
    ('JR', _('Jar')),
    ('KG', _('Kilogram')),
    ('DK', _('Kilometer')),
    ('KT', _('Kit')),
    ('LT', _('Liter')),
    ('MR', _('Meter')),
    ('MP', _('Metric Ton')),
    ('MC', _('Microgram')),
    ('4G', _('Microliter')),
    ('ME', _('Miligram')),
    ('ML', _('Mililiter')),
    ('MM', _('Milimeter')),
    ('OZ', _('Ounces')),
    ('PH', _('Pack')),
    ('PK', _('Package')),
    ('PA', _('Pail')),
    ('PR', _('Pair')),
    ('PL', _('Pallet')),
    ('P1', _('Percent')),
    ('PC', _('Piece')),
    ('PT', _('Pint')),
    ('PTN', _('Portion')),
    ('V2', _('Pouch')),
    ('ST', _('Set')),
    ('SH', _('Sheet')),
    ('SF', _('Square Foot')),
    ('SM', _('Square Meter')),
    ('SY', _('Square Yard')),
    ('TK', _('Tank')),
    ('TM', _('Thousand Feet')),
    ('UN', _('Unit')),
    ('YD', _('Yard')),
)

PRODUCT_DEFAULT_UOM = 'UN'

PRODUCT_SUPPLY_METHODS = (
    ('PUR', _('Purchase')),
    ('PROD', _('Production'))
)

PRODUCT_DEFAULT_SUPPLY_METHOD = 'PUR'

PRODUCT_DEFAULT_WARRANTY_PERIOD = 730
