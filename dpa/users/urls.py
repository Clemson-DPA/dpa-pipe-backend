from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^(?P<slug>\w+)/', views.ProfileView.as_view(), name='profile'),
)
