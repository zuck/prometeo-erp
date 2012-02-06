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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import list_detail, create_update
from django.views.generic.simple import redirect_to
from django.template import RequestContext
from django.contrib import messages

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.core.taxonomy.models import Vote

from ..models import *
from ..forms import *

def _get_poll(request, *args, **kwargs):
    id = kwargs.get('id', None)
    if id:
        return get_object_or_404(Poll, id=id)
    return None

@permission_required('knowledge.view_poll')
def poll_list(request, page=0, paginate_by=5, **kwargs):
    """Displays the list of all polls.
    """
    return filtered_list_detail(
        request,
        Poll,
        fields=['title', 'description', 'author', 'created'],
        paginate_by=paginate_by,
        page=page,
        **kwargs
    )   

@permission_required('knowledge.add_poll')
def poll_add(request, **kwargs):
    """Adds a new poll.
    """
    poll = Poll(author=request.user, language=request.user.get_profile().language)

    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        formset = ChoiceFormset(request.POST, instance=poll)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("The poll was created successfully."))
            return redirect_to(request, url=poll.get_absolute_url())
    else:
        form = PollForm(instance=poll)
        formset = ChoiceFormset(instance=poll)

    return render_to_response('knowledge/poll_edit.html', RequestContext(request, {'form': form, 'formset': formset, 'object': poll}))

@permission_required('knowledge.view_poll', _get_poll)
def poll_detail(request, id, **kwargs):
    """Displays the selected poll.
    """
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=Poll.objects.all(),
        **kwargs
    ) 

@permission_required('knowledge.view_poll', _get_poll)
@permission_required('taxonomy.add_vote')   
def poll_vote(request, id, choice, **kwargs):
    """Votes the selected choice.
    """
    from datetime import datetime

    poll = get_object_or_404(Poll, id=id)

    if poll.due_date is not None and poll.due_date < datetime.now():
        messages.warning(request, _("Sorry, this poll is already closed."))
        return redirect_to(request, permanent=False, url=poll.get_absolute_url())

    try:
        owner = request.user
        choices = poll.choices.all()
        choice_obj = choices[int(choice)]
        previous_vote = Vote.objects.get_for_models(choices).filter(owner=owner)
        if previous_vote.count() == 0:
            messages.success(request, _("Thank you for your vote."))
        else:
            previous_vote.delete()
            messages.success(request, _("Thank you. Your vote was updated successfully."))
        new_vote = Vote.objects.create(owner=owner, content_object=choice_obj)

    except IndexError:
        messages.error(request, _("Sorry, you selected an invalid choice."))

    return redirect_to(request, permanent=False, url=poll.get_absolute_url())

@permission_required('knowledge.change_poll', _get_poll)
def poll_edit(request, id, **kwargs):
    """Edits the given poll.
    """
    poll = get_object_or_404(Poll, id=id)

    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        formset = ChoiceFormset(request.POST, instance=poll)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _("The poll was updated successfully."))
            return redirect_to(request, url=poll.get_absolute_url())
    else:
        form = PollForm(instance=poll)
        formset = ChoiceFormset(instance=poll)

    return render_to_response('knowledge/poll_edit.html', RequestContext(request, {'form': form, 'formset': formset, 'object': poll}))

@permission_required('knowledge.delete_poll', _get_poll)
def poll_delete(request, id, **kwargs):
    """Deletes the given poll.
    """
    return create_update.delete_object(
        request,
        model=Poll,
        object_id=id,
        post_delete_redirect=reverse('poll_list'),
        template_name='knowledge/poll_delete.html',
        **kwargs
    )
