from django.db import models
from django.contrib.auth.models import User


class SecretFile(models.Model):
    """SecretFile class represents a ciphered file.
    Contains the file key, ciphered file and its owner.
    """
    # Filename, must not exceed 256 chars. Considered primary key
    name = models.CharField(max_length=256, primary_key=True)

    # IV is 128bit long, base64 encoded, which gives a maximum
    # length of aprox. 22 chars. Rounded up for safety.
    iv = models.CharField(max_length=30)

    # Key is 256bit long, base64 encoded, which gives a maximum
    # length of aprox. 43 chars. Rounded up for safety.
    # For testing only, final version should not save
    # the key (key will be ciphered)
    key = models.CharField(max_length=50)

    # Ciphertext field, base64 encoded, size varies.
    # For testing only, final version should not save
    # the CT (saved on the cloud instead)
    ct = models.TextField()

    # File owner reference, ignoring file sharing for now.
    owner = models.ForeignKey('CustomUser')

    def __unicode__(self):
        return self.name + " (" + str(self.owner) + ")"


class CustomUser(models.Model):
    """CustomUser class represents an app user.
    For now only links to Django's own user model
    """
    # Link to Django User model
    user = models.OneToOneField(User)

    # String representation of CustomUser shows
    # the username
    def __unicode__(self):
        return self.user.username
