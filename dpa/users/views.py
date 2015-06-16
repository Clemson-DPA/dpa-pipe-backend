from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import generic

class ProfileView(generic.DetailView):
    model = User
    slug_field = 'username'
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    # require login
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

