import io
from googleapiclient import errors
from googleapiclient.http import MediaIoBaseUpload
from .models import SecretFile
from sirs_users.models import CustomUser
from sirs_auth.auth_scripts import buildAndReturnDriveService



def downloadContentFromDrive(user,file):
    drive = buildAndReturnDriveService(user)
    id_file = file.iddrive
    content = drive.files().get_media(fileId=id_file).execute()
    return content


def uploadToDrive(user,file):
    drive = buildAndReturnDriveService(user)
    filestream = io.StringIO(file.ct)
    media_body = MediaIoBaseUpload(filestream, mimetype='txt/csv',resumable=True)
    
    body = {
    'title': file.name,
    'description': 'created by sirs app',
    'mimeType': 'txt/csv'}

    try:
        returnedfile = drive.files().insert(
        body=body,
        media_body=media_body).execute()

    # Uncomment the following line to print the File ID
    # print("File ID: ",file['id'])

        return returnedfile
    except errors.HttpError as error:
        print('error http - ', error)
        return None

def deleteFileFromDrive(user,file):
    drive = buildAndReturnDriveService(user)
    id_file = file.iddrive
    try:
        drive.files().delete(fileId=id_file).execute()
        return True
    except errors.HttpError as error:
        print('failed on deletion - ', error)
        return False

def updateFileOnDrive(user,file):
    drive = buildAndReturnDriveService(user)
    id_file = file.iddrive
    try:
        file_drive = drive.files().get(fileId=id_file).execute()
        file_drive['title'] = file.title
        
        filestream = io.StringIO(file.ct)
        media_body = MediaIoBaseUpload(filestream, mimetype='txt/csv',resumable=True)

        updated_file = service.files().update(
        fileId=id_file,
        body=file_drive,
        media_body=media_body).execute()
        return updated_file
    except errors.HttpError as error:
        print('failed on update ', error)
        return None