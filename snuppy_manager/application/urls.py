from django.conf.urls import url
from . import views


urlpatterns = [

    #APPLICATION URLS
    #add application
    url(r'application/add$', views.add_app, name='add_app'),
    url(r'application/add_app_check$', views.add_app_check, name='add_app_check'),
    #delete app
    url(r'application/delete', views.delete_app, name='delete_app'),
    #modify app
    url(r'application/$', views.change_app, name='change_app'),
    url(r'application/change', views.change_app_check, name='change_app_check'),

    ]
