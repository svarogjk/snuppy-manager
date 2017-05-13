from django.conf.urls import url
from . import views
from .views import ShowApp, AddApp, DeleteApp, ChangeApp


urlpatterns = [
    url(r'^$', ShowApp.as_view(), name='show_app'),
    url(r'^add$', AddApp.as_view(), name='add_app'),
    url(r'^delete', DeleteApp.as_view(), name='delete_app'),
    url(r'^change$', ChangeApp.as_view(), name='change_app'),
]
