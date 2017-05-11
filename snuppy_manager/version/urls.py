from django.conf.urls import url
from . import views


urlpatterns = [


    #VERSION URLS
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

    ]

