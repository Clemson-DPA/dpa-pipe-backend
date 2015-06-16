from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('ptasks',
    url(
        r'^types',
        views.PTaskTypeListView.as_view(),
		name='ptasktype_view'
    ),
    url(
        r'^timeline/(?P<pk>\d+)',  
        views.PTaskDetailView.as_view(template_name="ptask_timeline.html"), 
        name='ptask_timeline'
    ),
    url(
        r'^timeline/(?P<slug>[\w=]+)', 
        views.PTaskDetailView.as_view(template_name="ptask_timeline.html"), 
        name='ptask_timeline'
    ),
    url(
        r'^timeline/(?P<slug>[\w=]+)/(?P<level>[\w=]+)',
        'views.PTaskDetailView.filter_level'
    ),
	url(
		r'^detail/(?P<pk>\d+)',
		views.PTaskDetailView.as_view(template_name="ptask_detail.html"),
		name='ptask_detail'
	),
    url(
        r'^detail/(?P<slug>[\w=]+)', 
        views.PTaskDetailView.as_view(template_name="ptask_detail.html"),
        name='ptask_detail'
    ),
    url(
        r'^update/(?P<pk>\d+)',
        views.PTaskUpdateView.as_view(),
        name='ptask_update'
    ),
    url(
        r'^update/(?P<slug>[\w=]+)',
        views.PTaskUpdateView.as_view(),
        name='ptask_update'
    ),
)
