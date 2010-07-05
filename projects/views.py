#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision$'

from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext

from prometeo.core.details import ModelDetails, ModelPaginatedListDetails, value_to_string
from prometeo.core.paginator import paginate
from prometeo.core.search import search

from models import *
from forms import *
from details import *

@permission_required('projects.change_project')
def project_index(request):
    """Show a project list.
    """
    search_fields, projects = search(request, Project)
        
    projects = ModelPaginatedListDetails(request, projects, exclude=['id', 'description'])
        
    return render_to_response('projects/index.html', RequestContext(request, {'projects': projects, 'search_fields': search_fields}))

@permission_required('projects.add_project')     
def project_add(request):
    """Add a new project.
    """
    project = Project(author=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect_to(request, url=project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)

    return render_to_response('projects/add.html', RequestContext(request, {'form': form, 'project': project}));

@permission_required('projects.change_project')     
def project_view(request, id, page=None):
    """Show project details.
    """
    project = get_object_or_404(Project, pk=id)
    
    # Areas.
    if page == 'areas':
        areas = ModelPaginatedListDetails(request, project.area_set.all(), exclude=['id', 'description', 'project_id'])
        return render_to_response('projects/areas.html', RequestContext(request, {'project': project, 'areas': areas}))
        
    # Milestones.
    elif page == 'milestones':
        milestones = MilestoneListDetails(request, project.milestone_set.all(), exclude=['id', 'description', 'project_id'])
        return render_to_response('projects/milestones.html', RequestContext(request, {'project': project, 'milestones': milestones}))
        
    # Tickets.
    elif page == 'tickets':
        tickets = TicketListDetails(request, project.ticket_set.all(), exclude=['id', 'description', 'date_modified', 'project_id'])
        return render_to_response('projects/tickets.html', RequestContext(request, {'project': project, 'tickets': tickets}))
      
    # Members.  
    elif page == 'members':
        members = ModelPaginatedListDetails(request, project.membership_set.all(), exclude=['id', 'project_id'])
        return render_to_response('projects/members.html', RequestContext(request, {'project': project, 'members': members}))
        
    # Details.
    details = ModelDetails(instance=project, exclude=['id', 'description'])
    return render_to_response('projects/view.html', RequestContext(request, {'project': project, 'details': details, 'description': value_to_string(project.description)}))

@permission_required('projects.edit_project')     
def project_edit(request, id):
    """Edit a project.
    """
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect_to(request, url=project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)

    return render_to_response('projects/edit.html', RequestContext(request, {'form': form, 'project': project}));

@permission_required('projects.delete_project')
def project_delete(request, id):
    """Delete a project.
    """
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            project.delete()
            return redirect_to(request, url='/projects/');
        return redirect_to(request, url=project.get_absolute_url())
    return render_to_response('projects/delete.html', RequestContext(request, {'project': project}))

@permission_required('projects.add_area')
def area_add(request, project_id):
    """Add a new area.
    """
    project = get_object_or_404(Project, pk=project_id)
    area = Area(project=project, author=request.user)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            area = form.save()
            return redirect_to(request, url=area.get_absolute_url())
    else:
        form = AreaForm(instance=area)

    return render_to_response('projects/areas/add.html', RequestContext(request, {'form': form, 'area': area}));

@permission_required('projects.change_area')
def area_view(request, project_id, id, page=None):
    """Show area details.
    """
    project = get_object_or_404(Project, pk=project_id)
    area = get_object_or_404(Area, pk=id)
    if area.project != project:
        raise Http404
        
    # Tickets.
    if page == 'tickets':
        tickets = TicketListDetails(request, area.ticket_set.all(), exclude=['id', 'description', 'date_modified', 'project_id'])
        return render_to_response('projects/areas/tickets.html', RequestContext(request, {'area': area, 'tickets': tickets}))
      
    # Details.
    else:
        details = ModelDetails(instance=area, exclude=['id', 'description'])
        children = ModelPaginatedListDetails(request, area.area_set.all(), exclude=['id', 'description', 'project_id'])
        return render_to_response('projects/areas/view.html', RequestContext(request, {'area': area, 'details': details, 'children': children, 'description': value_to_string(area.description)}))

@permission_required('projects.change_area')
def area_edit(request, project_id, id):
    """Edit a area.
    """
    project = get_object_or_404(Project, pk=project_id)
    area = get_object_or_404(Area, pk=id)
    if area.project != project:
        raise Http404
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            area = form.save()
            return redirect_to(request, url=area.get_absolute_url())
    else:
        form = AreaForm(instance=area)

    return render_to_response('projects/areas/edit.html', RequestContext(request, {'form': form, 'area': area}));

@permission_required('projects.delete_area')
def area_delete(request, project_id, id):
    """Delete a area.
    """
    project = get_object_or_404(Project, pk=project_id)
    area = get_object_or_404(Area, pk=id)
    if area.project != project:
        raise Http404
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            area.delete()
            return redirect_to(request, url=project.get_areas_url());
        return redirect_to(request, url=area.get_absolute_url())
    return render_to_response('projects/areas/delete.html', RequestContext(request, {'area': area}))
    
@permission_required('projects.add_ticket')    
def area_ticket_add(request, project_id, id):
    """Add a new ticket to the area.
    """
    project = get_object_or_404(Project, pk=project_id)
    area = get_object_or_404(Area, pk=id)
    if area.project != project:
        raise Http404
        
    ticket = Ticket(project=project, author=request.user, area=area)
    if request.method == 'POST':
        form = AreaTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect_to(request, url=area.get_tickets_url())
    else:
        form = AreaTicketForm(instance=ticket)

    return render_to_response('projects/areas/add_ticket.html', RequestContext(request, {'area': area, 'form': form, 'ticket': ticket}));

@permission_required('projects.add_milestone')
def milestone_add(request, project_id):
    """Add a new milestone.
    """
    project = get_object_or_404(Project, pk=project_id)
    milestone = Milestone(project=project, author=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            return redirect_to(request, url=milestone.get_absolute_url())
    else:
        form = MilestoneForm(instance=milestone)

    return render_to_response('projects/milestones/add.html', RequestContext(request, {'form': form, 'milestone': milestone}));

@permission_required('projects.change_milestone')
def milestone_view(request, project_id, id, page=None):
    """Show milestone details.
    """
    project = get_object_or_404(Project, pk=project_id)
    milestone = get_object_or_404(Milestone, pk=id)
    if milestone.project != project:
        raise Http404
        
    # Tickets.
    if page == 'tickets':
        tickets = TicketListDetails(request, milestone.ticket_set.all(), exclude=['id', 'description', 'date_modified', 'project_id'])
        return render_to_response('projects/milestones/tickets.html', RequestContext(request, {'milestone': milestone, 'tickets': tickets}))
      
    # Details.
    else:
        details = ModelDetails(instance=milestone, exclude=['id', 'description'])
        children = MilestoneListDetails(request, milestone.milestone_set.all(), exclude=['id', 'description', 'project_id'])
        return render_to_response('projects/milestones/view.html', RequestContext(request, {'milestone': milestone, 'details': details, 'children': children, 'description': value_to_string(milestone.description)}))

@permission_required('projects.change_milestone')     
def milestone_edit(request, project_id, id):
    """Edit a milestone.
    """
    project = get_object_or_404(Project, pk=project_id)
    milestone = get_object_or_404(Milestone, pk=id)
    if milestone.project != project:
        raise Http404
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save()
            return redirect_to(request, url=milestone.get_absolute_url())
    else:
        form = MilestoneForm(instance=milestone)

    return render_to_response('projects/milestones/edit.html', RequestContext(request, {'form': form, 'milestone': milestone}));

@permission_required('projects.delete_milestone')    
def milestone_delete(request, project_id, id):
    """Delete a milestone.
    """
    project = get_object_or_404(Project, pk=project_id)
    milestone = get_object_or_404(Milestone, pk=id)
    if milestone.project != project:
        raise Http404
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            milestone.delete()
            return redirect_to(request, url=project.get_milestones_url());
        return redirect_to(request, url=milestone.get_absolute_url())
    return render_to_response('projects/milestones/delete.html', RequestContext(request, {'milestone': milestone}))
    
@permission_required('projects.add_ticket')    
def milestone_ticket_add(request, project_id, id):
    """Add a new ticket to the milestone.
    """
    project = get_object_or_404(Project, pk=project_id)
    milestone = get_object_or_404(Milestone, pk=id)
    if milestone.project != project:
        raise Http404
        
    ticket = Ticket(project=project, author=request.user, milestone=milestone)
    if request.method == 'POST':
        form = MilestoneTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect_to(request, url=milestone.get_tickets_url())
    else:
        form = MilestoneTicketForm(instance=ticket)

    return render_to_response('projects/milestones/add_ticket.html', RequestContext(request, {'milestone': milestone, 'form': form, 'ticket': ticket}));

@permission_required('projects.add_ticket')    
def ticket_add(request, project_id):
    """Add a new ticket.
    """
    project = get_object_or_404(Project, pk=project_id)
    ticket = Ticket(project=project, author=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect_to(request, url=ticket.get_absolute_url())
    else:
        form = TicketForm(instance=ticket)

    return render_to_response('projects/tickets/add.html', RequestContext(request, {'form': form, 'ticket': ticket}));

@permission_required('projects.change_ticket')     
def ticket_view(request, project_id, id):
    """Show ticket details.
    """
    project = get_object_or_404(Project, pk=project_id)
    ticket = get_object_or_404(Ticket, pk=id)
    if ticket.project != project:
        raise Http404
    details = ModelDetails(instance=ticket, exclude=['id', 'description'])
    return render_to_response('projects/tickets/view.html', RequestContext(request, {'ticket': ticket, 'details': details, 'description': value_to_string(ticket.description) }))

@permission_required('projects.change_ticket')     
def ticket_edit(request, project_id, id):
    """Edit a ticket.
    """
    project = get_object_or_404(Project, pk=project_id)
    ticket = get_object_or_404(Ticket, pk=id)
    if ticket.project != project:
        raise Http404
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect_to(request, url=ticket.get_absolute_url())
    else:
        form = TicketForm(instance=ticket)

    return render_to_response('projects/tickets/edit.html', RequestContext(request, {'form': form, 'ticket': ticket}));

@permission_required('projects.delete_ticket')    
def ticket_delete(request, project_id, id):
    """Delete a ticket.
    """
    project = get_object_or_404(Project, pk=project_id)
    ticket = get_object_or_404(Ticket, pk=id)
    if ticket.project != project:
        raise Http404
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            ticket.delete()
            return redirect_to(request, url=project.get_tickets_url());
        return redirect_to(request, url=ticket.get_absolute_url())
    return render_to_response('projects/tickets/delete.html', RequestContext(request, {'ticket': ticket}))
    
@permission_required('projects.add_member')    
def member_add(request, project_id):
    """Add a new member.
    """
    project = get_object_or_404(Project, pk=project_id)
    member = Membership(project=project)
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            return redirect_to(request, url=project.get_members_url())
    else:
        form = MembershipForm(instance=member)

    return render_to_response('projects/members/add.html', RequestContext(request, {'form': form, 'member': member}));
    
@permission_required('projects.member_ticket')    
def member_delete(request, project_id, id):
    """Delete a member.
    """
    project = get_object_or_404(Project, pk=project_id)
    member = get_object_or_404(Membership, pk=id)
    if member.project != project:
        raise Http404
    if request.method == 'POST':
        if (request.POST.has_key(u'yes')):
            member.delete()
            return redirect_to(request, url=project.get_members_url());
        return redirect_to(request, url=member.get_absolute_url())
    return render_to_response('projects/members/delete.html', RequestContext(request, {'member': member}))
