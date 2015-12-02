import os
import logging
import httplib2

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.shortcuts import Http404 
from sirs import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from sirs_auth.models import CredentialsModel
from googleapiclient import discovery


# Create your views here.


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/drive.file',
    redirect_uri='http://sirs.duckdns.org:8000/auth/oauth2callback')

@login_required
def redirectFlow(request):
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY.encode('utf-8'), request.user.username.encode('utf-8'))
    authorize_url = FLOW.step1_get_authorize_url()
    return redirect(authorize_url)

@login_required
def oauth2callback(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY.encode('utf-8'), request.GET.get('state').encode('utf-8'), request.user.username.encode('utf-8')):
        return  HttpResponse("Bad Request")
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return redirect("/")
