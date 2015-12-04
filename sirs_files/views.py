from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileUpload, FileDownload , FileAndUserSelection, FileShare
from .models import SecretFile , SharedSecretFile
from sirs_users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from sirs_files.file_scripts import uploadToDrive, downloadContentFromDrive, deleteFileFromDrive
import io
from django.contrib.auth.models import User
from sirs.settings import WEBPATH


files_path = WEBPATH + "files/"

share_path = files_path + "share/"

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
                  {'file_list':file_list, 'webpath' : WEBPATH})

@login_required
def sharecenter(request):
    return render(request,'sirs_files/sharecenter.html',{'webpath':WEBPATH, 'sharepath' : share_path})

@login_required
def sharerequests(request):
    owner = get_object_or_404(CustomUser, user=request.user)
    queryset = SharedSecretFile.objects.filter(destiny_user=owner)
    if not queryset:
        return HttpResponse("no pending requests")
    else:
        return render(request, 'sirs_files/sharerequests.html',{'file_list': queryset, 'webpath':WEBPATH, 'sharepath': share_path})


@login_required
def shareuserSelection(request):
    owner = get_object_or_404(CustomUser, user=request.user)
    form = FileAndUserSelection(get_my_choices(owner))
    return render(request, 'sirs_files/fileuserform.html',
                      {'form': form, 'sharepath' : share_path})

@login_required
def step2share(request):
    if request.method != 'POST':
        return redirect('sirs_files:shareuserSelection')
    else:
        form = FileAndUserSelection(get_my_choices(get_object_or_404(CustomUser,user=request.user)),request.POST)
        if form.is_valid() :
            owner = get_object_or_404(CustomUser, user=request.user)
            destiny_user = get_object_or_404(CustomUser, user = get_object_or_404(User, username= form.cleaned_data['username']))
            file = get_object_or_404(SecretFile,iddrive = form.cleaned_data['choices'])
            form2 = FileShare(initial={'pubKey': destiny_user.publicKey ,'key' : file.key, 'ct' : downloadContentFromDrive(request.user,file), 'iv' : file.iv , 'name' : file.name , 'username': form.cleaned_data['username'] })
            return render(request,"sirs_files/filesharefinal.html",{'form':form2 , 'sharepath' : share_path })
        return HttpResponse("Bad form")

@login_required
def sharingComplete(request):
    if request.method != 'POST':
        return redirect('sirs_files:shareuserSelection')
    else:
        form = FileShare(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.creator = get_object_or_404(CustomUser, user=request.user)
            file.destiny_user = get_object_or_404(CustomUser, user = get_object_or_404(User, username= form.cleaned_data['username']))
            file.save()
            return HttpResponse("File shared!")
        else:
            return HttpResponse("Failed to share file")


@login_required
def acceptRequest(request, shareid):
    currentUser = get_object_or_404(CustomUser,user=request.user)
    shareable = get_object_or_404(SharedSecretFile, id = shareid)
    if currentUser != shareable.destiny_user:
        HttpResponse("This is not your file")
    else:
        file = SecretFile()
        file.owner = currentUser
        file.name = shareable.name
        file.key = shareable.key
        file.iv = shareable.iv
        file.ct = shareable.ct
        uploadedfile = uploadToDrive(request.user,file)
        file.iddrive =  uploadedfile['id']
        file.lastmodified = uploadedfile['modifiedDate']
        file.ct = str()
        file.save()
        shareable.delete()
        return HttpResponse("File has been saved to your drive")


@login_required
def rejectRequest(request,shareid):
    currentUser = get_object_or_404(CustomUser,user=request.user)
    shareable = get_object_or_404(SharedSecretFile, id = shareid)
    if currentUser != shareable.destiny_user:
        HttpResponse("This is not your file")
    else:
        shareable.delete()
        return HttpResponse("Request has been deleted")

def get_my_choices(user):
    queryset = SecretFile.objects.filter(owner=user).values('iddrive','name','lastmodified')
    for x in queryset:
        print(x)
    return ((x['iddrive'], x['name'] +' '+ x['lastmodified']) for x in queryset)