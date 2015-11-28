from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileUpload, FileDownload
from .models import SecretFile
from sirs_users.models import CustomUser
from django.contrib.auth.decorators import login_required


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
def download(request, filename):
    """
    Takes an authenticated user and a filename and returns
    the iv, key and ct of that file
    """
    owner = get_object_or_404(CustomUser, user=request.user)
    queryset = SecretFile.objects.filter(owner=owner)
    file = get_object_or_404(queryset, name=filename)
    form = FileDownload(instance=file)
    return render(request, 'sirs_files/download.html',
                  {'form': form})
