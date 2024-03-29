﻿"""sirs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from sirs_auth import views
import sirs_main

urlpatterns = [
    url(r'^$', include('sirs_main.urls', namespace = 'sirs_main')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('sirs_auth.urls', namespace='sirs_auth')),
    url(r'^users/', include('sirs_users.urls', namespace='sirs_users')),
    url(r'^files/', include('sirs_files.urls', namespace='sirs_files')),
]
