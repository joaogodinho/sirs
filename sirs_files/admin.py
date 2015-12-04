from django.contrib import admin
from .models import SecretFile, SharedSecretFile


admin.site.register(SecretFile)
admin.site.register(SharedSecretFile)