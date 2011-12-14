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
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.conf import settings

from prometeo.core.auth.decorators import obj_permission_required as permission_required
from prometeo.core.views import filtered_list_detail
from prometeo.partners.models import Job

from ..forms import *

def _get_employee(request, *args, **kwargs):
    return get_object_or_404(Employee, id=kwargs.get('id', None))

@permission_required('hr.change_employee') 
def employee_list(request, page=0, paginate_by=10, **kwargs):
    """Displays the list of all filtered employees.
    """
    return filtered_list_detail(
        request,
        Employee,
        paginate_by=paginate_by,
        page=page,
        template_name='hr/employee_list.html',
        **kwargs
    )

@permission_required('hr.change_employee', _get_employee)  
def employee_detail(request, id, **kwargs):
    """Displays a employee.
    """
    object_list = Employee.objects.all()
    return list_detail.object_detail(
        request,
        object_id=id,
        queryset=object_list,
        template_name=kwargs.pop('template_name', 'hr/employee_detail.html'),
        extra_context={'object_list': object_list},
        **kwargs
    )
 
@permission_required('hr.add_employee')    
def employee_add(request, **kwargs):
    """Adds a new employee.
    """
    job = Job()
    employee = Employee()
      
    if request.method == 'POST':
        jform = JobForm(request.POST, instance=job)
        form = EmployeeForm(request.POST, instance=employee)
        if jform.is_valid():
            jform.save()
            employee = job.employee
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                messages.success(request, _("The employee has been saved."))
                return redirect_to(request, url=employee.get_absolute_url())
            else:
                job.delete()
                jform = JobForm(instance=job)
                form = EmployeeForm(instance=employee)
    else:
        jform = JobForm(instance=job)
        form = EmployeeForm(instance=employee)

    return render_to_response('hr/employee_edit.html', RequestContext(request, {'form': form, 'jform': jform, 'object': employee}))

@permission_required('hr.change_employee', _get_employee)  
def employee_edit(request, id, **kwargs):
    """Edits a employee.
    """
    employee = get_object_or_404(Employee, id=id)
    job = employee.job
        
    if request.method == 'POST':
        jform = JobForm(request.POST, instance=job)
        form = EmployeeForm(request.POST, instance=employee)
        if jform.is_valid() and form.is_valid():
            jform.save()
            form.save()
            messages.success(request, _("The employee has been updated."))
            return redirect_to(request, url=employee.get_absolute_url())
    else:
        jform = JobForm(instance=job)
        form = EmployeeForm(instance=employee)

    return render_to_response('hr/employee_edit.html', RequestContext(request, {'form': form, 'jform': jform, 'object': employee}))

@permission_required('hr.delete_employee', _get_employee) 
def employee_delete(request, id, **kwargs):
    """Deletes a employee.
    """
    return create_update.delete_object(
        request,
        Job,
        object_id=Employee.objects.get(id=id).job.pk,
        post_delete_redirect=reverse('employee_list'),
        template_name='hr/employee_delete.html',
        **kwargs
    )
