from django.conf.urls import include, patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login/', 
        'django.contrib.auth.views.login',
        {
            'template_name': '_site/login.html'
        },
        name='login'
    ),
    url(r'^logout/', 
        'django.contrib.auth.views.logout',
        {
            'template_name': '_site/logout.html',
            'next_page': '/',
        },
        name='logout'
    ),
)

