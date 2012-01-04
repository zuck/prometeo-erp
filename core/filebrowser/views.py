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

import os
import shutil

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings

from base import *
from models import *
from forms import *

if not os.access(settings.MEDIA_ROOT, os.F_OK):
    os.makedirs(settings.MEDIA_ROOT)

def serve(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/serve.html', **kwargs):
    """Serves files or directories.
    """
    if request.GET:
        request.session['GET'] = request.GET

    fi = FileInfo(url_to_path(url or settings.MEDIA_URL))

    # The path points to a folder.
    if fi.is_folder():
        extra_context = {'fileinfo': fi, 'root': root}
        extra_context.update(kwargs.get('extra_context', {}))
        
        return render_to_response(template_name, RequestContext(request, extra_context))

    # The path points to a file.
    else:
        fd = open(fi.abspath, 'rb')
        response = HttpResponse(fd.readlines(), mimetype=fi.mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % fi.name
        if fi.size is not None:
            response['Content-Length'] = fi.size

        return response

def mkdir(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/mkdir.html', **kwargs):
    """Makes a new folder at the given url.
    """
    fi = FileInfo(url_to_path('/%s' % url))

    if request.method == 'POST': 
        form = NameForm(fi.abspath, request.POST) 

        if form.is_valid():
            name = form.cleaned_data['name']
            os.mkdir(os.path.join(fi.abspath, name))
            messages.success(request, _('The folder "%(name)s" was created succesfully.') % {'name': name})

            return redirect(path_to_url(fi.abspath))
    else:
        form = NameForm(fi.abspath)

    extra_context = {'fileinfo': fi, 'root': root, 'form': form}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))

def upload(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/upload.html', **kwargs):
    """Uploads a new file to the given url.
    """
    fi = FileInfo(url_to_path('/%s' % url))

    if request.method == 'POST': 
        form = UploadForm(fi.abspath, data=request.POST, files=request.FILES) 

        if form.is_valid(): 
            filename = form.cleaned_data['name'] or form.cleaned_data['file'].name
            file_path = os.path.join(fi.abspath, filename)
            destination = open(file_path, 'wb+')
            for chunk in form.cleaned_data['file'].chunks():
                destination.write(chunk)
            messages.success(request, _('The file "%(filename)s" was uploaded succesfully.') % {'filename': filename})

            return redirect(path_to_url(fi.abspath))
    else:
        form = UploadForm(fi.abspath)

    extra_context = {'fileinfo': fi, 'root': root, 'form': form}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))

def move(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/move.html', **kwargs):
    """Moves a file, folder or link to a new location.
    """
    fi = FileInfo(url_to_path('/%s' % url))

    if request.method == 'POST': 
        form = DestinationForm(fi.abspath, request.POST) 
        if form.is_valid():
            destination = form.cleaned_data['destination']
            new_path = os.path.join(destination, fi.name)
            
            if new_path != fi.abspath:
                shutil.move(fi.abspath, new_path)
                messages.success(request, _('"%(name)s" was moved succesfully to "%(dest)s".') % {'name': fi.name, 'dest': path_to_url(destination)})

            return redirect(path_to_url(destination))
    else:
        form = DestinationForm(fi.abspath, initial={'destination': get_parent(fi.abspath)})

    extra_context = {'fileinfo': fi, 'root': root, 'form': form}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))

def copy(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/copy.html', **kwargs):
    """Copies a file, folder or link [to another location].
    """
    fi = FileInfo(url_to_path('/%s' % url))

    if request.method == 'POST': 
        form = NameDestinationForm(fi.abspath, request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            name = form.cleaned_data.get('name', None) or fi.name
            new_path = os.path.join(destination, name)

            if new_path != fi.abspath:
                if fi.is_folder():
                    shutil.copytree(fi.abspath, new_path)
                else:
                    shutil.copy(fi.abspath, new_path)
                messages.success(request, _('A copy of "%(name)s" was created succesfully.') % {'name': fi.name})

            return redirect(path_to_url(destination))
    else:
        form = NameDestinationForm(fi.abspath, initial={'destination': get_parent(fi.abspath), 'name': fi.copy_name})

    extra_context = {'fileinfo': fi, 'root': root, 'form': form}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))

def mkln(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/mkln.html', **kwargs):
    """Makes a new link to the given url.
    """
    fi = FileInfo(url_to_path('/%s' % url))

    if request.method == 'POST': 
        form = NameDestinationForm(fi.abspath, request.POST) 
        if form.is_valid():
            destination = form.cleaned_data['destination']
            name = form.cleaned_data.get('name', None) or fi.name
            new_path = os.path.join(destination, name)

            if new_path != fi.abspath:
                os.symlink(fi.abspath, new_path)
                messages.success(request, _('The link to "%(name)s" was created succesfully.') % {'name': fi.name})

            return redirect(path_to_url(destination))
    else:
        form = NameDestinationForm(fi.abspath, initial={'name': "Link to %s" % fi.name, 'destination': get_parent(fi.abspath)})

    extra_context = {'fileinfo': fi, 'root': root, 'form': form}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))

def rename(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/rename.html', **kwargs):
    """Renames a file, folder or link.
    """
    fi = FileInfo(url_to_path('/%s' % url))

    if request.method == 'POST': 
        form = NameForm(fi.parent.abspath, request.POST) 
        if form.is_valid():
            redirect_to = fi.parent.url
            new_path = os.path.join(fi.parent.abspath, form.cleaned_data['name'])
            os.rename(fi.abspath, new_path)
            islink = fi.is_link()
            isdir = fi.is_folder()
            if islink:
                messages.success(request, _('The link was renamed succesfully.'))
            elif isdir:
                messages.success(request, _('The folder was renamed succesfully.'))
            else:
                messages.success(request, _('The file was renamed succesfully.'))

            return redirect(redirect_to)
    else:
        form = NameForm(fi.parent.abspath, initial={'name': fi.name})

    extra_context = {'fileinfo': fi, 'root': root, 'form': form}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))

def delete(request, url, root=settings.MEDIA_ROOT, template_name='filebrowser/delete.html', **kwargs):
    """Deletes a file, folder or link.
    """
    fi = FileInfo(url_to_path('/%s' % url))
    islink = fi.is_link()
    isdir = fi.is_folder()

    if request.method == 'POST':
        redirect_to = fi.parent.url
        if islink:
            os.remove(fi.abspath)
            messages.success(request, _('The link was deleted successfully.'))
        elif isdir:
            shutil.rmtree(fi.abspath)
            messages.success(request, _('The folder was deleted successfully.'))
        else:
            os.remove(fi.abspath)
            messages.success(request, _('The file was deleted successfully.'))
        return redirect(redirect_to)

    extra_context = {'fileinfo': fi, 'root': root}
    extra_context.update(kwargs.get('extra_context', {}))

    return render_to_response(template_name, RequestContext(request, extra_context))
