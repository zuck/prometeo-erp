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

# Inspired by http://code.google.com/p/django-nav/

import re
from django import template

from prometeo.core.menu import menubar

register = template.Library()

class GetMenuNode(template.Node):
    def __init__(self, menu_group, var_name):
            self.menu_group = menu_group
            self.var_name = var_name
            self.context = {'request': ''}

    def render(self, context):
        self.context = context        
        self.build_menu()
        return ''

    def build_menu(self):
        self.context[self.var_name] = []

        for menu in menubar[self.menu_group]:
            print menu
            menu_info = {
                'group': menu.group,
                'name': menu.name,
                'link': menu.link,
                'active': (self.context['request'].path == menu.link),
                'option_list': self.build_options(menu.options)
            }

            self.context[self.var_name].append(template.loader.render_to_string(menu.template, {'menu': menu_info}))

    def build_options(self, tab_options):
        options = []
        for option in tab_options:
            option.option_list = self.build_options(option.options)
            options.append(template.loader.render_to_string(option.template, {'option': option}))

        return options

@register.tag
def get_menu(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    m = re.search(r'(.*?) as (\w+)', args)
    if not m:
        menu_group = var_name = args.strip("'").strip('"')
    else:
        menu_group, var_name = m.groups()
        menu_group = menu_group.strip("'").strip('"')

    return GetMenuNode(menu_group, var_name)
