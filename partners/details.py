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

from django.utils.translation import ugettext_lazy as _

from prometeo.core import details

class ExtendedModelDetails(details.ModelDetails):
    def __init__(self, instance, fields=[], exclude=['id']):
        super(ExtendedModelDetails, self).__init__(instance, fields, exclude)
        
        # Add addresses as field instances.
        if details.is_visible('addresses', fields, exclude):
            for i, address in enumerate(instance.addresses.all()):
                type = address.get_type_display()
                addr = details.value_to_string(address)
                self.add_field(_('Address #%(num)s (%(type)s)') % {'num': i+1, 'type': type}, addr)
        
        # Add telephones as field instances.
        if details.is_visible('telephones', fields, exclude):
            for i, telephone in enumerate(instance.telephones.all()):
                type = telephone.get_type_display()
                tel = details.value_to_string(telephone)
                self.add_field(_('Telephone #%(num)s (%(type)s)') % {'num': i+1, 'type': type}, tel)
    

class ContactDetails(ExtendedModelDetails):
    pass

class PartnerDetails(ExtendedModelDetails):
    pass
    
class ContactListDetails(details.ModelPaginatedListDetails):
    pass

class PartnerListDetails(details.ModelPaginatedListDetails):
    def row_template(self, row, index):
        i = self._header.index(_('managed'))
        if row[i]:
            return u'\t<tr class="managed">\n'
        return super(PartnerListDetails, self).row_template(row, index)
        
    def column_template(self, row, index):
        i = self._header.index(_('managed'))
        j = self._header.index(_('name'))
        if index == j and row[i]:
            value = row[index]
            return u'\t\t<td class="name"><span class="sign">(*)</span>%s</td>\n' % details.value_to_string(value)
        return super(PartnerListDetails, self).column_template(row, index)
        
class PartnerJobListDetails(PartnerListDetails):
    def __init__(self, request, queryset=[], fields=[], exclude=['id'], with_actions=True):
        super(PartnerJobListDetails, self).__init__(request, [j.partner for j in queryset], fields, exclude, with_actions)
        if details.is_visible('role'):
            self._header.insert(-1, _('Role'))
            for i, instance in enumerate(queryset):
                role = details.value_to_string(details.field_to_value(instance._meta.fields[3], instance))
                self._rows[i].insert(-1, role)

class ContactJobListDetails(ContactListDetails):
    def __init__(self, request, queryset=[], fields=[], exclude=['id'], with_actions=True):
        super(ContactJobListDetails, self).__init__(request, [j.contact for j in queryset], fields, exclude, with_actions)
        if details.is_visible('role'):
            self._header.insert(-1, _('Role'))
            for i, instance in enumerate(queryset):
                role = details.value_to_string(details.field_to_value(instance._meta.fields[3], instance))
                self._rows[i].insert(-1, role)
