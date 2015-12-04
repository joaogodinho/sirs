from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/$',views.filemain, name='filemain'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^download/(?P<iddrive>.*)$', views.download, name='download'),
    url(r'^delete/(?P<iddrive>.*)$', views.delete, name='delete'),
    url(r'^details/(?P<iddrive>.*)$', views.details, name='details'),
    url(r'^share/$', views.sharecenter, name = 'share'),
    url(r'^share/upload/$',views.shareuserSelection, name = 'shareupload'),
    url(r'^share/upload/step2$',views.step2share, name = 'step2share'),
    url(r'^share/upload/sharingComplete$',views.sharingComplete, name = 'sharingComplete'),
    url(r'^share/requests/$',views.sharerequests, name = 'sharerequests'),
    url(r'^share/requests/accept/(?P<shareid>.*)$', views.acceptRequest, name='acceptRequest'),
    url(r'^share/requests/reject/(?P<shareid>.*)$', views.rejectRequest, name='rejectRequest')
]