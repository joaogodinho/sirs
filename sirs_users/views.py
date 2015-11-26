from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import FileUpload, FileDownload
from .models import CustomUser, SecretFile


# Takes an authenticated user and saves
# the given file
def upload(request):
    if request.user.is_authenticated():
        print request.user
        if request.method == 'POST':
            form = FileUpload(request.POST)
            if form.is_valid():
                owner = get_object_or_404(CustomUser, user=request.user)
                file = form.save(commit=False)
                file.owner = owner
                file.save()
                return redirect('sirs_users:upload')
            else:
                return render(request, 'sirs_users/upload.html',
                              {'form': form})
        else:
            form = FileUpload()
            return render(request, 'sirs_users/upload.html',
                          {'form': form})
    else:
        return HttpResponse("NO PERMISSION")


# Takes an authenticated user and a filename and returns
# the iv, key and ct of that file
def download(request, filename):
    if request.user.is_authenticated():
        owner = get_object_or_404(CustomUser, user=request.user)
        queryset = SecretFile.objects.filter(owner=owner)
        file = get_object_or_404(queryset, name=filename)
        form = FileDownload(instance=file)
        return render(request, 'sirs_users/download.html',
                      {'form': form})
    else:
        return HttpResponse("NO PERMISSION")
    return render(request, 'sirs_users/download.html')
