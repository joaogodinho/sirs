from django.contrib import admin
from sirs_auth.models import CredentialsModel, CredentialsAdmin
# Register your models here.


admin.site.register(CredentialsModel, CredentialsAdmin)