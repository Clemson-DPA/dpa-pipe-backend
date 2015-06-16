from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.urls import api_router

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('_site.urls', namespace="site")),
    url(r'^auth/', include('_site.urls', namespace="auth")),
    url(r'^locations/', include('locations.urls', namespace="locations")),
    url(r'^ptasks/', include('ptasks.urls', namespace="ptasks")),
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_router.urls)),
    url(r'^api2/', include('rest_framework_swagger.urls')),
)

