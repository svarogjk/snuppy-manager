from django.conf.urls import url
from . import views

urlpatterns = [


    #GROUP
    url(r'application/group$', views.show_groups, name='show_group'),
    url(r'application/group/add_new', views.group_add, name='group_add'),
    url(r'application/group/check_add', views.group_check_add, name='group_check_add'),
    url(r'application/group/edit', views.group_edit, name='group_edit'),
    url(r'application/group/add_user', views.group_add_user, name='group_add_user'),
    url(r'application/group/delete', views.group_delete, name='group_delete'),
    url(r'application/group/accept_invite', views.accept_invite, name='accept_invite'),
    url(r'application/group/decline_invite', views.decline_invite, name='decline_invite'),
    url(r'application/group/modify', views.group_modify, name='group_modify'),


    ]
