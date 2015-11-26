from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^upload/', views.upload, name='upload'),
    url(r'^download/(?P<filename>.+)$', views.download, name='download')
]
