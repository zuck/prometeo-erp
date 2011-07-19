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
__version__ = '0.0.2'

import codecs
import mimetypes
import os
import shutil

from datetime import datetime
from grp import getgrgid
from pwd import getpwuid

from django import http, template
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _

import forms
import utils

if not os.access(utils.get_upload_root(), os.F_OK):
    os.mkdir(utils.get_upload_root())

@staff_member_required
def admin_copy(request, url=None):
    """Copies file/directory to a new location.
    """

    # Not really happy about the l/rstrips.
    url = utils.clean_path(url)

    parent = '/'.join(url.split('/')[:-1])
    full_parent = os.path.join(utils.get_upload_root(), parent).rstrip('/')
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))
    directory = url.replace(parent, "", 1).lstrip('/')

    if request.method == 'POST': 
        form = forms.CopyForm(full_path, '', directory, full_path, request.POST) 
        if form.is_valid(): 
            new_path = os.path.join(form.cleaned_data['parent'],
                                    form.cleaned_data['name'])
            
            if os.path.isdir(full_path):
                shutil.copytree(full_path, new_path)
            else:
                shutil.copy(full_path, new_path)

            return redirect('admin_wysiwyg_list', url=utils.strip_path(parent))
    else:
        form = forms.CopyForm(full_path, '', directory, full_path, initial={'parent':full_parent, 'name': directory}) 

    return render_to_response("admin/wysiwyg/copy.html", 
                              {'form': form, 'url': url,
                               'current': "/%s" % parent,
                               'directory': os.path.isdir(full_path)},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_index(request, url=None):
    """Shows list of files in a url inside of the upload root.
    """
    # Stores the request GET dict for callback processing.
    if request.GET:
        request.session['GET'] = request.GET
        
    if request.method == 'POST': 
        if request.POST.get('action') == 'delete_selected':
            response = admin_delete_selected(request, url)
            if response:
                return response

    # Stuff the files in here.
    files = []
    directory = {}
    perms = [ '---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx' ]

    url = utils.clean_path(url)
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))

    try:
        listing = os.listdir(full_path)
    except OSError:
        raise http.Http404

    directory['url'] = url
    directory['parent'] = '/'.join(url.split('/')[:-1])

    if os.access(full_path, os.R_OK):
        directory['can_read'] = True
    else:
        directory['can_read'] = False 
    
    if os.access(full_path, os.W_OK):
        directory['can_write'] = True
    else:
        directory['can_write'] = False

    for file in listing:
        item = {}
        dperms = '-'
        
        item['filename'] = file
        item['filepath'] = os.path.join(full_path, file)
        item['fileurl'] = os.path.join(url, file)
        item['link_src'] = os.path.join(url, file)

        # type (direcory/file/link)
        item['directory'] = os.path.isdir(item['filepath'])
        item['link'] = os.path.islink(item['filepath'])

        if item['link']:
            item['link_src'] = os.path.normpath(os.path.join(url, os.readlink(item['filepath'])))
            if item['directory']:
                item['fileurl'] = os.path.normpath(os.path.join(url, os.readlink(item['filepath']))).lstrip('/')
            else:
                item['fileurl'] = os.path.normpath(os.path.join(utils.get_upload_url(), utils.strip_path(url), os.readlink(item['filepath']))).lstrip('/')
            
        # File url
        if not (item['directory'] or item['link']):
            item['fileurl'] = os.path.join(utils.get_upload_url(), item['fileurl'])[1:]

        # Catch broken links.
        try: 
            itemstat = os.stat(item['filepath'])
            
            item['user'] = getpwuid(itemstat.st_uid)[0]
            item['group'] = getgrgid(itemstat.st_gid)[0]

            # size (in bytes ) for use with |filesizeformat
            if item['directory']:
                item['size'] = 0
                for dirpath, dirnames, filenames in os.walk(item['filepath']):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            item['size'] += os.path.getsize(fp)
            else:
                item['size'] = itemstat.st_size

            # ctime, mtime
            item['ctime'] = datetime.fromtimestamp(itemstat.st_ctime)
            item['mtime'] = datetime.fromtimestamp(itemstat.st_mtime)

            # permissions (numeric)
            octs = "%04d" % int(oct(itemstat.st_mode & 0777))
            item['perms_numeric'] = octs
            item['perms'] = "%s%s%s%s" % (dperms, perms[int(octs[1])], 
                                            perms[int(octs[2])], 
                                            perms[int(octs[3])])

        except:
            # Blank out because of broken link.
            item['user'] = item['group'] = ''
            item['perms_numeric'] = item['perms'] = ''
            item['size'] = item['ctime'] = item['mtime'] = None
            item['broken_link'] = True

        mime = mimetypes.guess_type(item['filepath'], False)[0]
  
        # Assume we can't edit anything except text and unknown.
        if not mime:
            item['can_edit'] = True
        elif 'text' in mime:
            item['can_edit'] = True
        else:
            item['can_edit'] = False

        if item['directory']:
            item['can_edit'] = False
            dperms = 'd'

     
        if os.access(item['filepath'], os.R_OK):
            item['can_read'] = True
        else:
            item['can_read'] = False

        if os.access(item['filepath'], os.W_OK):
            item['can_write'] = True
        else:
            item['can_write'] = False

        files.append(item)
    
    return render_to_response("admin/wysiwyg/index.html", 
                              {'directory': directory, 'files': files,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_mkln(request, url=None):
    """Makes a new link at the current url.
    """

    url = utils.clean_path(url)
    full_path = os.path.join(utils.get_upload_root(), url)

    if request.method == 'POST': 
        form = forms.CreateLinkForm(full_path, None, full_path, request.POST) 

        if form.is_valid(): 
            src = os.path.join(full_path, form.cleaned_data['link'])
            dest = os.path.join(full_path, form.cleaned_data['name'])
            
            try:
                relative = os.path.relpath(src, full_path)
            except AttributeError:
                relative = utils.relpath(src, full_path)

            os.symlink(relative, dest)
            
            return redirect('admin_wysiwyg_list', url=url)
    else:
        form = forms.CreateLinkForm(full_path, None, full_path)

    return render_to_response("admin/wysiwyg/mkln.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_mkdir(request, url=None):
    """Makes a new directory at the current url.
    """

    url = utils.clean_path(url)
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))

    if request.method == 'POST': 
        form = forms.NameForm(full_path, None, request.POST) 

        if form.is_valid(): #Make the directory
            os.mkdir(os.path.join(full_path, form.cleaned_data['name']))

            return redirect('admin_wysiwyg_list', url=url)
    else:
        form = forms.NameForm(full_path, None) # An unbound form 

    return render_to_response("admin/wysiwyg/mkdir.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_delete_selected(request, url=None):
    """Deletes selected files and directories. 
    
    This view is called from index.
    """
   
    # Files to remove.
    selected = request.POST.getlist('_selected_action')
    
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))
    full_parent = os.path.join(utils.get_upload_root(), parent).rstrip('/')

    if request.method == 'POST' and request.POST.get('post') == 'yes':
        # Files selected to remove.
       
        for item in selected:
            full_path = os.path.join(full_parent, item)

            # If this is a directory, do the walk
            if os.path.isdir(full_path) and not os.path.islink(full_path):
                for root, dirs, files in os.walk(full_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))

                os.rmdir(full_path)
            else:
                os.remove(full_path)

        return None

    filelist = []
    errorlist = []

    for item in selected:
        full_path = os.path.join(full_parent, item)

        # If this is a directory, generate the list of files to be removed.
        if os.path.isdir(full_path) and not os.path.islink(full_path):
            filelist.append("/%s" % item)
            for root, dirs, files, in os.walk(full_path):
                for name in files: 
                    f = os.path.join(root, name).replace(full_parent, '', 1)
                    if not os.access(os.path.join(root), os.W_OK):
                        errorlist.append(f)
                    filelist.append(f)

                for name in dirs:
                    d = os.path.join(root, name).replace(full_parent, '', 1)
                    if not os.access(os.path.join(root), os.W_OK):
                        errorlist.append(d)
                    filelist.append(d)
        else:
            if not os.access(full_path, os.W_OK):
                errorlist.append("/%s" % item)

            filelist.append("/%s" % item)

    # Because python 2.3 is ... painful.
    filelist.sort()
    errorlist.sort()
    
    return render_to_response("admin/wysiwyg/delete_selected.html", 
                              {'files': filelist,
                               'errorlist': errorlist,
                               'selected': selected,
                               'directory': '',},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_delete(request, url=None):
    """Deletes a file/directory.
    """
    
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))
    full_parent = os.path.join(utils.get_upload_root(), parent).rstrip('/')

    if request.method == 'POST': 
        
        # If this is a directory, do the walk
        if os.path.isdir(full_path) and not os.path.islink(full_path):
            for root, dirs, files in os.walk(full_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(full_path)
        else:
            os.remove(full_path)

        return redirect('admin_wysiwyg_list', url=utils.strip_path(parent))

    filelist = []
    errorlist = []

    # If this is a directory, generate the list of files to be removed.
    if os.path.isdir(full_path) and not os.path.islink(full_path):
        filelist.append("/%s" % url)
        for root, dirs, files, in os.walk(full_path):
            for name in files: 
                f = os.path.join(root, name).replace(full_parent, '', 1)
                if not os.access(os.path.join(root), os.W_OK):
                    errorlist.append(f)
                filelist.append(f)

            for name in dirs:
                d = os.path.join(root, name).replace(full_parent, '', 1)
                if not os.access(os.path.join(root), os.W_OK):
                    errorlist.append(d)
                filelist.append(d)
    else:
        if not os.access(full_path, os.W_OK):
            errorlist.append("/%s" % url)

        filelist.append("/%s" % url)

    # Because python 2.3 is ... painful.
    filelist.sort()
    errorlist.sort()
    
    return render_to_response("admin/wysiwyg/delete.html", 
                             # {'url': url, 'files': sorted(filelist),
                             #  'errorlist':sorted(errorlist),
                              {'url': url, 'files': filelist,
                               'errorlist': errorlist,
                               'directory': '',},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_move(request, url=None):
    """Moves file/directory to a new location.
    """

    # Not really happy about the l/rstrips.
    url = utils.clean_path(url)

    parent = '/'.join(url.split('/')[:-1])
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))
    full_parent = os.path.join(utils.get_upload_root(), parent).rstrip('/')
    directory = url.replace(parent, "", 1).lstrip('/')

    if request.method == 'POST': 
        form = forms.DirectoryForm(directory, full_path, request.POST) 

        if form.is_valid(): 
            new = os.path.join(form.cleaned_data['parent'], directory)

            if os.path.islink(full_path):

                src = os.readlink(full_path)
                if not os.path.isabs(src):
                    src = os.path.join(os.path.dirname(full_path), src)

                try:
                    relative = os.path.relpath(src, form.cleaned_data['parent'])
                except AttributeError:
                    relative = utils.relpath(src, form.cleaned_data['parent'])

                os.remove(full_path) # Remove original link.
                os.symlink(relative, new) # Create new link.

            else:
                os.rename(full_path, new) #Rename the directory

            return redirect('admin_wysiwyg_list', url=utils.strip_path(parent))
    else:
        form = forms.DirectoryForm(directory, full_path, initial={'parent':full_parent}) 

    return render_to_response("admin/wysiwyg/move.html", 
                              {'form': form, 'url': url,
                               'current': "/%s" % parent,
                               'directory': os.path.isdir(full_path)},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_rename(request, url=None):
    """Renames a file/directory.
    """

    # Not really happy about the l/rstrips.
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_parent = os.path.join(utils.get_upload_root(), parent).rstrip('/')
    full_path = os.path.join(utils.get_upload_root(), utils.strip_path(url))

    if request.method == 'POST': 
        form = forms.NameForm(full_parent, full_path, request.POST) 

        if form.is_valid(): 
            new = os.path.join(full_parent, form.cleaned_data['name'])

            # Rename 
            os.rename(full_path, new)

            return redirect('admin_wysiwyg_list', url=utils.strip_path(parent))
    else:
        directory = url.replace(parent, "", 1).lstrip('/')
        data = {'name':directory}
        form = forms.NameForm(full_parent, full_path, initial=data)

    return render_to_response("admin/wysiwyg/rename.html", 
                              {'form': form, 'url': url, 
                               'directory': os.path.isdir(full_path)},
                              context_instance=template.RequestContext(request))

@staff_member_required
#@csrf_exempt
def admin_upload(request, url=None):
    """Uploads a new file.
    """
    url = utils.clean_path(url)
    path = os.path.join(utils.get_upload_root(), utils.strip_path(url))

    if request.method == 'POST': 
        form = forms.UploadForm(path, data=request.POST, files=request.FILES) 

        if form.is_valid(): 
            file_path = os.path.join(path, form.cleaned_data['name'] or form.cleaned_data['file'].name)
            destination = open(file_path, 'wb+')
            for chunk in form.cleaned_data['file'].chunks():
                destination.write(chunk) 

            return redirect('admin_wysiwyg_list', url=url)
    else:
        form = forms.UploadForm(path)

    return render_to_response("admin/wysiwyg/upload.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def admin_select(request, url=None):
    """Selects a file.
    """
    url = '/' + utils.clean_path(url)
    
    GET = request.session['GET']
    del request.session['GET']

    return HttpResponse('<html><head><script type="text/javascript">        \
	function selectFile()                                                   \
    {                                                                       \
	    window.top.opener.CKEDITOR.tools.callFunction(%s, encodeURI("%s")); \
	    window.top.close();                                                 \
	    window.top.opener.focus();                                          \
    }                                                                       \
    window.onload = selectFile;                                             \
	</script></head></html>' % (GET['CKEditorFuncNum'], url))
