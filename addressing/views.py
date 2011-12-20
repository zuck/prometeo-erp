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
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.simple import redirect_to
from django.views.generic import create_update
from django.db import models

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from models import *
from forms import *

def _get_address(request, *args, **kwargs):
    return get_object_or_404(Address, id=kwargs.get('object_id', None))

def _get_phone_num(request, *args, **kwargs):
    return get_object_or_404(PhoneNumber, id=kwargs.get('object_id', None))

def _get_social_profile(request, *args, **kwargs):
    return get_object_or_404(SocialProfile, id=kwargs.get('object_id', None))

def _get_field_and_value(owner, owner_field):
    """Returns the field object and the value of the given field.
    """
    rel = owner._meta.get_field_by_name(owner_field)[0]
    value = getattr(owner, owner_field)

    return rel, value  

@permission_required('addressing.view_address')
def address_list(request, template_name, page=0, paginate_by=10, owner=None, owner_field='addresses', **kwargs):
    """Returns the filtered list of [the given owner's] addresses.
    """
    queryset = Address.objects.all()

    if owner:
        rel, value = _get_field_and_value(owner, owner_field)
        if isinstance(rel, models.ForeignKey):
            queryset = Address.objects.filter(id=value.pk)
        elif isinstance(rel, models.ManyToManyField):
            queryset = value.all()
    
    return filtered_list_detail(request, queryset, exclude=['id'], template_name=template_name, **kwargs)

@permission_required('addressing.add_address')    
def address_add(request, owner, post_save_redirect, template_name, owner_field='addresses', **kwargs):
    """Adds a new address to the given owner.
    """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save()
            rel, value = _get_field_and_value(owner, owner_field)
            if isinstance(rel, models.ForeignKey):
                setattr(owner, owner_field, instance)
            elif isinstance(rel, models.ManyToManyField):
                value.add(instance)
            owner.save()
            if owner.pk:
                messages.success(request, _("Address added to %(owner)s") % {'owner': owner})
            return redirect_to(request, url=post_save_redirect)
    else:
        form = AddressForm()

    context = {'owner': owner, 'form': form}
    if 'extra_context' in kwargs:
        context.update(kwargs['extra_context'])

    return render_to_response(template_name, RequestContext(request, context))

@permission_required('addressing.change_address', _get_address)    
def address_edit(request, object_id, post_save_redirect, template_name, **kwargs):
    """Edits an address.
    """
    instance = get_object_or_404(Address, id=object_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _("Address updated"))
            return redirect_to(request, url=post_save_redirect)
    else:
        form = AddressForm(instance=instance)

    context = {'object': instance, 'form': form}
    if 'extra_context' in kwargs:
        context.update(kwargs['extra_context'])

    return render_to_response(template_name, RequestContext(request, context))

@permission_required('addressing.delete_address', _get_address)    
def address_delete(request, object_id, post_delete_redirect, template_name, **kwargs):
    """Deletes an address.
    """
    return create_update.delete_object(
        request,
        model=Address,
        object_id=object_id,
        post_delete_redirect=post_delete_redirect,
        template_name=template_name,
        **kwargs
    )

@permission_required('addressing.view_phonenumber')
def phone_number_list(request, template_name, page=0, paginate_by=10, owner=None, owner_field='phone_numbers', **kwargs):
    """Returns the filtered list of [the given owner's] phone numbers.
    """
    queryset = PhoneNumber.objects.all()

    if owner:
        rel, value = _get_field_and_value(owner, owner_field)
        if isinstance(rel, models.ForeignKey):
            queryset = PhoneNumber.objects.filter(id=value.pk)
        elif isinstance(rel, models.ManyToManyField):
            queryset = value.all()
    
    return filtered_list_detail(request, queryset, exclude=['id'], template_name=template_name, **kwargs)

@permission_required('addressing.add_phonenumber')    
def phone_number_add(request, owner, post_save_redirect, template_name, owner_field='phone_numbers', **kwargs):
    """Adds a new phone number to the given owner.
    """
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            instance = form.save()
            rel, value = _get_field_and_value(owner, owner_field)
            if isinstance(rel, models.ForeignKey):
                setattr(owner, owner_field, instance)
            elif isinstance(rel, models.ManyToManyField):
                value.add(instance)
            owner.save()
            if owner.pk:
                messages.success(request, _("Phone number added to %(owner)s") % {'owner': owner})
            return redirect_to(request, url=post_save_redirect)
    else:
        form = PhoneNumberForm()

    context = {'owner': owner, 'form': form}
    if 'extra_context' in kwargs:
        context.update(kwargs['extra_context'])

    return render_to_response(template_name, RequestContext(request, context))

@permission_required('addressing.change_phonenumber', _get_phone_num)    
def phone_number_edit(request, object_id, post_save_redirect, template_name, **kwargs):
    """Edits a phone number.
    """
    instance = get_object_or_404(PhoneNumber, id=object_id)

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _("Phone number updated"))
            return redirect_to(request, url=post_save_redirect)
    else:
        form = PhoneNumberForm(instance=instance)

    context = {'object': instance, 'form': form}
    if 'extra_context' in kwargs:
        context.update(kwargs['extra_context'])

    return render_to_response(template_name, RequestContext(request, context))

@permission_required('addressing.delete_phonenumber', _get_phone_num)    
def phone_number_delete(request, object_id, post_delete_redirect, template_name, **kwargs):
    """Deletes a phone number.
    """
    return create_update.delete_object(
        request,
        model=PhoneNumber,
        object_id=object_id,
        post_delete_redirect=post_delete_redirect,
        template_name=template_name,
        **kwargs
    )

@permission_required('addressing.view_socialprofile')
def social_profile_list(request, template_name, page=0, paginate_by=10, owner=None, owner_field='social_profiles', **kwargs):
    """Returns the filtered list of [the given owner's] social profiles.
    """
    queryset = SocialProfile.objects.all()

    if owner:
        rel, value = _get_field_and_value(owner, owner_field)
        if isinstance(rel, models.ForeignKey):
            queryset = SocialProfile.objects.filter(id=value.pk)
        elif isinstance(rel, models.ManyToManyField):
            queryset = value.all()
    
    return filtered_list_detail(request, queryset, exclude=['id'], template_name=template_name, **kwargs)

@permission_required('addressing.add_socialprofile')    
def social_profile_add(request, owner, post_save_redirect, template_name, owner_field='social_profiles', **kwargs):
    """Adds a new social profile to the given owner.
    """
    if request.method == 'POST':
        form = SocialProfileForm(request.POST)
        if form.is_valid():
            instance = form.save()
            rel, value = _get_field_and_value(owner, owner_field)
            if isinstance(rel, models.ForeignKey):
                setattr(owner, owner_field, instance)
            elif isinstance(rel, models.ManyToManyField):
                value.add(instance)
            owner.save()
            if owner.pk:
                messages.success(request, _("Social profile added to %(owner)s") % {'owner': owner})
            return redirect_to(request, url=post_save_redirect)
    else:
        form = SocialProfileForm()

    context = {'owner': owner, 'form': form}
    if 'extra_context' in kwargs:
        context.update(kwargs['extra_context'])

    return render_to_response(template_name, RequestContext(request, context))

@permission_required('addressing.change_socialprofile', _get_social_profile)    
def social_profile_edit(request, object_id, post_save_redirect, template_name, **kwargs):
    """Edits a social profile.
    """
    instance = get_object_or_404(SocialProfile, id=object_id)

    if request.method == 'POST':
        form = SocialProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _("Social profile updated"))
            return redirect_to(request, url=post_save_redirect)
    else:
        form = SocialProfileForm(instance=instance)

    context = {'object': instance, 'form': form}
    if 'extra_context' in kwargs:
        context.update(kwargs['extra_context'])

    return render_to_response(template_name, RequestContext(request, context))

@permission_required('addressing.delete_socialprofile', _get_social_profile)    
def social_profile_delete(request, object_id, post_delete_redirect, template_name, **kwargs):
    """Deletes a social profile.
    """
    return create_update.delete_object(
        request,
        model=SocialProfile,
        object_id=object_id,
        post_delete_redirect=post_delete_redirect,
        template_name=template_name,
        **kwargs
    )
