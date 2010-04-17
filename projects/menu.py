#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

from django.utils.translation import ugettext_lazy as _
from prometeo.core.menu import Menu, menubar

menubar.register(Menu(_('Projects'), '/projects/', 'projects'))
