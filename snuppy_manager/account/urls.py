from django.conf.urls import url
from django.conf import settings
from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static

from django.contrib.auth.views import (login, logout,
                                       logout_then_login, password_change,
                                       password_change_done,
                                       password_reset, password_reset_done,
                                       password_reset_confirm, password_reset_complete)


urlpatterns = [


    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^register/$', views.register, name='register'),

    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),

    #change password urls
    url(r'^password-change/$',
            password_change,
            name='password_change'),
    url(r'^password-change/done/$',
        password_change_done,
        name='password_change_done'),

    #show versions for selected app
    url(r'version/$', views.show_version, name='show_version'),
    #add version
    url(r'version/add_new$', views.add_version, name='add_version'),
    #send data for compile new version
    url(r'version/compile_ver', views.compile_ver, name='compile_ver'),
    #modify or remove version
    url(r'version/modify', views.modify_ver, name='modify_ver'), #not used now...
    url(r'version/change', views.change_ver, name='change_ver'),
    url(r'version/delete', views.delete_ver, name='delete_ver'),

    #add application
    url(r'application/add$', views.add_app, name='add_app'),
    url(r'application/add_app_check$', views.add_app_check, name='add_app_check'),
    #delete app
    url(r'application/delete', views.delete_app, name='delete_app'),
    #modify app
    url(r'application/$', views.change_app, name='change_app'),
    url(r'application/change', views.change_app_check, name='change_app_check'),

    #restore password urls
    url(r'^password-reset/$',
        password_reset,
        name='password_reset'),

    url(r'^password-reset/done/$',
            password_reset_done,
            name='password_reset_done'),

    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm,
        name='password_reset_confirm'),

    url(r'^password-reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
]




