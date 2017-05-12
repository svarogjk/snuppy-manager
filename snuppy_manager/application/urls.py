from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.show, name='show_app'),
    url(r'^add$', views.add_app, name='add_app'),
    url(r'^change$', views.change_app, name='change_app'),
    url(r'^delete', views.delete_app, name='delete_app'),
]
