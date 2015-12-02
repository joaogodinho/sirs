from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.redirectFlow, name = 'begin_auth'),
    url(r'^oauth2callback', views.oauth2callback, name= 'callback'),
]
