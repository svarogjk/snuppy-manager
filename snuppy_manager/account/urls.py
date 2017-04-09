from django.conf.urls import url
from . import views

from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login

urlpatterns = [

    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),

    url(r'^$', views.dashboard, name='dashboard'),
]


