from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sirs_auth.auth_scripts import hasValidCredentials

@login_required
def home(request):
    if hasValidCredentials(request.user):
        return render(request,'sirs_main/homepage.html')
    else: return redirect('sirs_auth:begin_auth')
