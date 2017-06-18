from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_groups, name='show_group'),
    url(r'^add$', views.group_add, name='group_add'),
    url(r'^edit$', views.group_edit, name='group_edit'),
    url(r'^delete$', views.group_delete, name='group_delete'),

    url(r'^invite/user$', views.group_add_user, name='group_add_user'),
    url(r'^invite/accept$', views.accept_invite, name='accept_invite'),
    url(r'^invite/decline$', views.decline_invite, name='decline_invite'),
]
