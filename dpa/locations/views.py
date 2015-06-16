from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Location

class ListView(generic.ListView):
    template_name = 'locations/loc_list.html'
    context_object_name = 'location_list'

    def get_queryset(self):
        """Return all locations."""
        return Location.objects.order_by('name')

    # require login
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)

class MapView(generic.DetailView):
    model = Location
    template_name = 'locations/loc_map.html'

    # require login
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MapView, self).dispatch(*args, **kwargs)

