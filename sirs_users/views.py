from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserCustomCreationForm
from django.contrib.auth import login as djangoLogin, logout as djangoLogout
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    """
    Registers a user and redirects him to the homepage
    """
    if request.user.is_authenticated():
        return redirect('sirs_main:home')
    userForm = UserCreationForm()
    userCustomForm = UserCustomCreationForm()
    if request.method == 'POST':
        userForm = UserCreationForm(request.POST)
        userCustomForm = UserCustomCreationForm(request.POST)
        if userForm.is_valid() and userCustomForm.is_valid():
            with transaction.atomic():
                user = userForm.save()
                userCustom = userCustomForm.save(commit=False)
                userCustom.user = user
                userCustom.save()
            return redirect('sirs_main:home')
    return render(request, 'sirs_users/register.html',
                  {'register_form': userForm,
                   'register_customform': userCustomForm})


def login(request):
    """
    Allows a user to login and redirects him to the provided
    'next' page. If already logged in just redirects.
    """
    next = request.GET.get('next', '/')
    if request.user.is_authenticated():
        return redirect(next)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            djangoLogin(request, user)
            return redirect(next)
        else:
            return render(request, 'sirs_users/login.html', {'login_form': form})
    else:
        return render(request, 'sirs_users/login.html', {'login_form': AuthenticationForm()})


def logout(request):
    """
    Logs out a user and redirects him to the login page
    """
    djangoLogout(request)
    return redirect('sirs_users:login')
