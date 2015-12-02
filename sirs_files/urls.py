from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/$',views.filemain, name='filemain'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^details/(?P<iddrive>.*)$', views.details, name='details'),
    url(r'^download/(?P<iddrive>.*)$', views.download, name='download'),
    url(r'^update/(?P<iddrive>.*)$', views.update, name='update'),
    url(r'^delete/(?P<iddrive>.*)$', views.delete, name='delete'),
]