from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ShowVersion.as_view(), name='show_version'),
    url(r'add$', views.add_version, name='add_version'),
    url(r'edit', views.edit, name='change_ver'),
    url(r'delete', views.delete_ver, name='delete_ver'),

]

