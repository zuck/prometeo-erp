#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

import os
from django.conf import settings

if not hasattr(settings, 'TEMPLATE_DIRS'):
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)
