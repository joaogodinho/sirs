from django.contrib import admin
from .models import CustomUser, SecretFile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__')

admin.site.register(CustomUser)
admin.site.register(SecretFile)
