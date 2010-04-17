#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.
"""

__author__ = 'Emanuele Bertoldi <e.bertoldi@card-tech.it>'
__copyright__ = 'Copyright (c) 2010 Card Tech srl'
__version__ = '$Revision: 4 $'

from issues.models import Issue

from django.db.models import Q

class IssueSearch(object):
    def __init__(self, search_data):
        self.__dict__.update(search_data)

    def search_keywords(self, q):
        """
        Search should do both title and description, and OR the results together, and must iterate over list of keywords
        """
        if self.keywords:
            words = self.keywords.split()
            title_q = Q()
            desc_q = Q()
            for word in words:
                title_q = title_q | Q(title__icontains=word)
                desc_q = desc_q | Q(description__icontains=word)
            keyword_q = title_q | desc_q
            q = q & keyword_q
        return q
    
    def search_date_added(self, q):
        if self.date_added:
            q = q & Q(date_added__exact=self.date_added)
        return q
        
    def search_date_modified(self, q):
        if self.date_modified:
            q = q & Q(date_modified__exact=self.date_modified)
        return q
        
    def search_date_completed(self, q):
        if self.date_completed:
            q = q & Q(date_completed__exact=self.date_completed)
        return q
        
    def search_date_due(self, q):
        if self.date_due:
            q = q & Q(date_due__exact=self.date_due)
        return q
        
    def search_status(self, q):
        if self.status:
            q = q & Q(status__iexact=self.status)
        return q
        
    def search_urgency(self, q):
        if self.urgency:
            q = q & Q(urgency__iexact=self.urgency)
        return q
        
    def search_importance(self, q):
        if self.importance:
            q = q & Q(importance__iexact=self.importance)
        return q
        
    def search_creator(self, q):
        if self.creator:
            q = q & Q(creator__icontains=self.creator)
        return q
        
    def search_owner(self, q):
        if self.owner:
            q = q & Q(owner__icontains=self.owner)
        return q
        
    def search_stakeholder(self, q):
        if self.stakeholder:    
            if isinstance(self.stakeholder, list):
                q = q & Q(stakeholder__in=self.stakeholder)
            else:
                q = q & Q(stakeholder__icontains=self.stakeholder)
        return q

def search(search_data):
    q = Q()
    results = None
    searcher = IssueSearch(search_data)
    
    for key in search_data.iterkeys():
        dispatch = getattr(searcher, 'search_%s' % key)
        q = dispatch(q)
    
    if q and len(q):
        results = Issue.objects.filter(q).select_related() #.order_by('-pk')
    else:
        results = []
    return results
