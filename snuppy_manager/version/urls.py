from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ShowVersion.as_view(), name='show_version'),
    url(r'delete', views.delete_ver, name='delete_ver'),

]
