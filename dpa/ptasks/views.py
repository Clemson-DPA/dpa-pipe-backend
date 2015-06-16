#------------------------------------------------------------------------------
# Module: dpa.ptasks.views
# Author: Gina Guerrero (gguerre), Josh Tomlinson (jtomlin)
#------------------------------------------------------------------------------
""" Defines all views for dpa ptasks.

Classes
-------

PTaskDetailView
    /ptasks/[spec|pk]
    Detailed information for project tasks

"""

#------------------------------------------------------------------------------
# Imports:
#------------------------------------------------------------------------------
import datetime
from datetime import date

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from .models import PTaskType, PTask, PTaskAssignment, PTaskVersion

#------------------------------------------------------------------------------
# Public Classes:
#------------------------------------------------------------------------------
#class MonthlyCalendarMixin(generic.dates.MonthArchiveView):
    #queryset = PTask.objects.filter(active=True)
    #date_field = 'due_date'
    #make_object_list = True
    #allow_future = True
#------------------------------------------------------------------------------
class PTaskDetailView(generic.DetailView):

    #--------------------------------------------------------------------------
    # Fields:
    #--------------------------------------------------------------------------
    model = PTask
    slug_field = 'spec'
    template_name = 'ptasks/ptask_detail.html', 'ptasks/ptask_timeline.html'
    context_object_name = 'ptask'
    
    #--------------------------------------------------------------------------
    # Public methods:
    #--------------------------------------------------------------------------
    # require login
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PTaskDetailView, self).dispatch(*args, **kwargs)
    
    # gathers necessary data for view
    def get_context_data(self, **kwargs):
        context = super(PTaskDetailView, self).get_context_data(**kwargs)
        # needed for versions
        context['versions'] = PTaskVersion.objects.filter(
            ptask=self.get_object()).order_by('-number')
        # needed for assigned users
        context['users'] = PTaskAssignment.objects.filter(
            ptask=self.get_object())
        # for calendar
        context['today'] = date.today()
        context['days_left'] = \
            (self.get_object().due_date-date.today()).days
        context['days_since'] = \
            (date.today()-self.get_object().start_date).days
        context['duration'] = \
            (self.get_object().due_date - self.get_object().start_date).days
        from_date = date(1970,1,1);
        context['to_start_date'] = (self.get_object().start_date - from_date).days+1
        # context['due_date'] = (self.get_object().due_date)
        return context

    def filter_level(request):
        return request.GET['level']
        
#-----------------------------------------------------------------------------
class PTaskUpdateView(generic.UpdateView):
    
    #--------------------------------------------------------------------------
    # Fields
    #--------------------------------------------------------------------------
    model = PTask
    slug_field = 'spec'
    fields = ['name', 'description', 'ptask_type', 'priority', 'status']
    template_name = 'ptasks/ptask_update.html'

#------------------------------------------------------------------------------
class PTaskTypeListView(generic.ListView):

    #--------------------------------------------------------------------------
    # Fields:
    #--------------------------------------------------------------------------
    model = PTaskType
    template_name = 'ptasks/ptasktype_list.html'
    
    #--------------------------------------------------------------------------
    # Public methods:
    #--------------------------------------------------------------------------
    # require login
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PTaskTypeListView, self).dispatch(*args, **kwargs)
    
    # gathers necessary data for view
    def get_queryset(self):
        """Return all locations."""
        return PTaskType.objects.order_by('level_hint')

# class TimelineView():
#     #--------------------------------------------------------------------------
#     # Fields:
#     #--------------------------------------------------------------------------
#     model = PTask
#     template_name = 'ptasks/ptask_timeline.html'
    
#     #--------------------------------------------------------------------------
#     # Public methods:
#     #--------------------------------------------------------------------------
#     # require login
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(TimelineView, self).dispatch(*args, **kwargs)

#     # # gathers necessary data for view
#     # def get_context_data(self, **kwargs):
#     #     context = super(DetailView, self).get_context_data(**kwargs)
#     #     # needed for versions
#     #     context['start_date'] = PTaskVersion.objects.start_date
#     #     context['end_date'] = PTaskVersion.objects.end_date
#     #     return context
