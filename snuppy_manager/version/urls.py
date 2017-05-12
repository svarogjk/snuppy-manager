from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'version/$', views.show_version, name='show_version'),
    url(r'version/add$', views.add_version, name='add_version'),
    url(r'version/edit', views.edit, name='change_ver'),
    url(r'version/delete', views.delete_ver, name='delete_ver'),

    # send data for compile new version
    url(r'version/compile_ver', views.compile_ver, name='compile_ver'),
]

