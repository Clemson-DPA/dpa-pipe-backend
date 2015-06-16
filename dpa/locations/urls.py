from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='loc_list'),
    url(r'^(?P<pk>\w+)/map/$', views.MapView.as_view(), name='loc_map'),
)

