from sirs_auth.models import CredentialsModel
from oauth2client.django_orm import Storage
from googleapiclient.discovery import build
import httplib2

def hasValidCredentials(user):
    credential = getCredentials(user)
    if credential is None or credential.invalid == True:
        return False
    return True

def getCredentials(user):
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()
    return credential

def buildAndReturnDriveService(user):
    credential = getCredentials(user)
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("drive", "v2", http=http)
    return service