from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    """CustomUser class represents an app user.
    Links to Django's own user model and holds a public key field
    """
    # Link to Django User model
    user = models.OneToOneField(User)

    # User public key
    publicKey = models.CharField(max_length=256, default="")

    # String representation of CustomUser shows
    # the username
    def __unicode__(self):
        return self.user.username
