from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^(?P<user_id>[0-9]+)/$', views.show_all_app, name='show_all_app'),
    # url(r'^logout/$',
    #     views.logout,
    #     name='logout'),
    # url(r'^logout-then-login/$',
    #     views.logout_then_login,
    #     name='logout_then_login'),
]