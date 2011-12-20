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

import re

from django.db import models
from django.db.models import Q
from django.db.models.loading import get_models
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages

from prometeo.core.utils import clean_referer
from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail

from models import *
from forms import *

LOADING = False
MODELS = {}

def autodiscover():
    """ Auto discover search indexes of installed applications.
    """
    global LOADING
    global MODELS
    
    if LOADING:
        return
    
    LOADING = True

    import imp
    
    for model in get_models():
        if '.'.join([model._meta.app_label, model.__name__]) in getattr(settings, 'SEARCH_IN_MODELS', []):
            fields = model._meta.fields
            for field in fields:
                if isinstance(field, (models.fields.CharField, models.fields.TextField)):
                    if not model in MODELS:
                        MODELS[model] = []
                    MODELS[model].append(field)
        
    LOADING = False

def _normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'(\s{2,})').sub):
    """Splits the query string in invidual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
       
    Example:
        
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string.replace('+', ' '))] 

def _get_query(query_string, search_fields):
    """Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.
    """
    query = None # Query to search for every search term        
    terms = _normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def _get_category(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    return get_object_or_404(Category, slug=slug)

def _get_tag(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    return get_object_or_404(Tag, slug=slug)

def search(request, query_string="", page=0, paginate_by=10, **kwargs):
    """Displays the list of results for the current search query.
    """
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        return redirect_to(request, reverse('search_with_query', args=[query_string.replace(' ', '+')]))
       
    Result.objects.all().delete() 
    if query_string:
        autodiscover()
        for model, fields in MODELS.items():
            q = _get_query(query_string, [field.name for field in fields])
            objects = model.objects.filter(q)
            for obj in objects:
                r = Result(title=obj, content_object=obj)
                r.save()
    else:
        messages.error(request, _("Please, specify a valid search query."))
            
    return list_detail.object_list(
        request,
        queryset=Result.objects.all(),
        paginate_by=paginate_by,
        page=page,
        template_name="taxonomy/search.html",
        extra_context={'query': query_string.replace('+', ' ')},
        **kwargs
    )

@permission_required('taxonomy.view_category') 
def category_list(request, page=0, paginate_by=5, **kwargs):
    """Displays the list of all categories.
    """
    return filtered_list_detail(
        request,
        Category.objects.filter(parent=None),
        fields=['title', 'parent'],
        paginate_by=paginate_by,
        page=page,
        **kwargs
    )

@permission_required('taxonomy.add_category')    
def category_add(request, **kwargs):
    """Adds a new category.
    """
    referer = clean_referer(request)
    if referer == reverse("tag_list"):
        referer = None

    return create_update.create_object(
        request,
        form_class=CategoryForm,
        post_save_redirect=referer,
        template_name='taxonomy/category_edit.html'
    )

@permission_required('taxonomy.view_category', _get_category) 
def category_detail(request, slug, page=0, paginate_by=10, **kwargs):
    """Displays the selected category.
    """
    Result.objects.all().delete()
    object_list = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    for obj in category.occurences:
        r = Result(title=obj, content_object=obj)
        r.save()
    return list_detail.object_list(
        request,
        queryset=Result.objects.all(),
        paginate_by=paginate_by,
        page=page,
        template_name="taxonomy/category_detail.html",
        extra_context={'categories': object_list, 'object': category},
        **kwargs
    )

@permission_required('taxonomy.change_category', _get_category)    
def category_edit(request, slug, **kwargs):
    """Edits a category.
    """
    return create_update.update_object(
        request,
        slug=slug,
        form_class=CategoryForm,
        template_name='taxonomy/category_edit.html'
    )

@permission_required('taxonomy.delete_category', _get_category)     
def category_delete(request, slug, **kwargs):
    """Deletes a category.
    """
    return create_update.delete_object(
            request,
            model=Category,
            slug=slug,
            post_delete_redirect='/categories/',
            template_name='taxonomy/category_delete.html',
            **kwargs
        )

@permission_required('taxonomy.view_tag') 
def tag_list(request, page=0, paginate_by=5, **kwargs):
    """Displays the list of all tags.
    """
    return filtered_list_detail(
        request,
        Tag.objects.all(),
        fields=['title'],
        paginate_by=paginate_by,
        page=page,
        **kwargs
    )

@permission_required('taxonomy.add_tag')    
def tag_add(request, **kwargs):
    """Adds a new tag.
    """
    referer = clean_referer(request)
    if referer == reverse("tag_list"):
        referer = None

    return create_update.create_object(
        request,
        form_class=TagForm,
        post_save_redirect=referer,
        template_name='taxonomy/tag_edit.html'
    )

@permission_required('taxonomy.view_tag', _get_tag)  
def tag_detail(request, slug, page=0, paginate_by=10, **kwargs):
    """Displays the selected tag.
    """
    Result.objects.all().delete()
    object_list = Tag.objects.all()
    tag = get_object_or_404(Tag, slug=slug)
    for obj in tag.occurences:
        r = Result(title=obj, content_object=obj)
        r.save()
    return list_detail.object_list(
        request,
        queryset=Result.objects.all(),
        paginate_by=paginate_by,
        page=page,
        template_name="taxonomy/tag_detail.html",
        extra_context={'tags': object_list, 'object': tag},
        **kwargs
    )

@permission_required('taxonomy.change_tag', _get_tag)    
def tag_edit(request, slug, **kwargs):
    """Edits a tag.
    """
    return create_update.update_object(
        request,
        slug=slug,
        form_class=TagForm,
        template_name='taxonomy/tag_edit.html'
    )

@permission_required('taxonomy.delete_tag', _get_tag)     
def tag_delete(request, slug, **kwargs):
    """Deletes a tag.
    """
    return create_update.delete_object(
            request,
            model=Tag,
            slug=slug,
            post_delete_redirect='/tags/',
            template_name='taxonomy/tag_delete.html',
            **kwargs
        )
