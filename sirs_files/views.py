from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileUpload, FileDownload
from .models import SecretFile
from sirs_users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from sirs_files.file_scripts import uploadToDrive, downloadContentFromDrive, deleteFileFromDrive
import io


web_path = "http://sirs.duckdns.org:8000/"

files_path = web_path + "files/"

@login_required
def upload(request):
    """
    Takes an authenticated user and saves
    the given file
    """
    owner = get_object_or_404(CustomUser, user=request.user)
    if request.method == 'POST':
        form = FileUpload(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = owner
            uploadedfile = uploadToDrive(request.user,file)
            file.iddrive = uploadedfile['id']
            file.lastmodified = uploadedfile['modifiedDate']
            file.ct = str() #erase file content
            file.save()
            return redirect('sirs_files:upload')
        else:
            return render(request, 'sirs_files/upload.html',
                          {'form': form})
    else:
        form = FileUpload(initial={'pubKey': owner.publicKey})
        return render(request, 'sirs_files/upload.html',
                      {'form': form})



# Takes an authenticated user and a filename and returns
# the iv, key and ct of that file
@login_required
def download(request, iddrive):
    """
    Takes an authenticated user and a filename and returns
    the iv, key and ct of that file
    """
    owner = get_object_or_404(CustomUser, user=request.user)
    queryset = SecretFile.objects.filter(owner=owner)
    file = get_object_or_404(queryset, iddrive=iddrive)
    file.ct = downloadContentFromDrive(request.user,file)
    form = FileDownload(instance=file)
    file.ct = str()
    return render(request, 'sirs_files/download.html',
                  {'form': form})

@login_required
def details(request,iddrive):

    owner = get_object_or_404(CustomUser, user=request.user)
    queryset = SecretFile.objects.filter(owner=owner)
    file = get_object_or_404(queryset, iddrive=iddrive)
    return render(request, 'sirs_files/details.html',
                  {'file' : file , 'webpath' : files_path})

@login_required
def update(request,iddrive):
    return HttpResponse("hello update")

@login_required
def delete(request, iddrive):
    owner = get_object_or_404(CustomUser, user=request.user)
    queryset = SecretFile.objects.filter(owner=owner)
    file = get_object_or_404(queryset, iddrive=iddrive)
    if deleteFileFromDrive(request.user,file):
        queryset.delete()
        return redirect("/")
    else:
        return HttpResponse("Failed to delete file ", file.name)

@login_required
def filemain(request):
    owner = get_object_or_404(CustomUser,user=request.user)
    file_list = SecretFile.objects.filter(owner=owner)
    return render(request, 'sirs_files/list.html',
                  {'file_list':file_list, 'webpath' : web_path})
