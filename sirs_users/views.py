from django.shortcuts import render
from django.http import HttpResponse


def upload(request):
    # TODO: take json POST request with file
    return HttpResponse("Hello from upload")


def download(request):
    # TODO: answer with file in json
    return HttpResponse("Hello from download")
