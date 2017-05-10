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

    #dashboard
    url(r'^$', views.dashboard, name='dashboard'),

    #register
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

    #group
    url(r'application/group$', views.show_groups, name='show_group'),
    url(r'application/group/add_new', views.group_add, name='group_add'),
    url(r'application/group/check_add', views.group_check_add, name='group_check_add'),
    url(r'application/group/edit', views.group_edit, name='group_edit'),
    url(r'application/group/add_user', views.group_add_user, name='group_add_user'),
    url(r'application/group/delete', views.group_delete, name='group_delete'),
    url(r'application/group/accept_invite', views.accept_invite, name='accept_invite'),
    url(r'application/group/decline_invite', views.decline_invite, name='decline_invite'),
    url(r'application/group/modify', views.group_modify, name='group_modify'),

    #accept_invite

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




