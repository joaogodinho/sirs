from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from oauth2client.django_orm import CredentialsField


class CredentialsAdmin(admin.ModelAdmin):
    pass

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key = True)
    credential = CredentialsField()
