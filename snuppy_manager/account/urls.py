from django.conf.urls import url
from django.conf import settings
from django.conf.urls import include, url
from . import views

from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_change

urlpatterns = [

    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),

    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^(?P<user_id>[0-9]+)/$', views.show_all_app, name='show_all_app'),
    url(r'^password-change/$',
        password_change,
        name='password_change'),
    url(r'^password-change/done/$',
        password_change_done,
        name='password_change_done'),

    #restore password urls
    url(r'^password-reset/$',)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


