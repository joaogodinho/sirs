from django.db import models


class SecretFile(models.Model):
    """SecretFile class represents a ciphered file.
    Contains the file key, ciphered file and its owner.
    """
    # Filename, must not exceed 256 chars. Considered primary key
    name = models.CharField(max_length=256, primary_key=True)

    # IV is 128bit long, base64 encoded, which gives a maximum
    # length of aprox. 22 chars. Rounded up for safety.
    iv = models.CharField(max_length=30)

    # Key represents {Key}PubKey, is base64 encoded
    key = models.CharField(max_length=350)

    # Ciphertext field, base64 encoded, size varies.
    # For testing only, final version should not save
    # the CT (saved on the cloud instead)
    ct = models.TextField()

    # File owner reference, ignoring file sharing for now.
    owner = models.ForeignKey('sirs_users.CustomUser')

    def __unicode__(self):
        return self.name + " (" + str(self.owner) + ")"
