from django.db import models
from django.db.models.options import Options




class SecretFile(models.Model):
    """SecretFile class represents a ciphered file.
    Contains the file key, ciphered file and its owner.
    """
    
    id = models.AutoField(primary_key=True)

    # Filename, must not exceed 256 chars. Considered primary key
    name = models.CharField(max_length=256)

    iddrive = models.TextField()

    # IV is 128bit long, base64 encoded, which gives a maximum
    # length of aprox. 22 chars. Rounded up for safety.
    iv = models.CharField(max_length=30)

    lastmodified = models.TextField()
    # Key is 256bit long, base64 encoded, which gives a maximum
    # length of aprox. 43 chars. Rounded up for safety.
    # For testing only, final version should not save
    # the key (key will be ciphered)
    key = models.CharField(max_length=350)

    # Ciphertext field, base64 encoded, size varies.
    # For testing only, final version should not save
    # the CT (saved on the cloud instead)
    ct = models.TextField()

    # File owner reference, ignoring file sharing for now.
    owner = models.ForeignKey('sirs_users.CustomUser')

    class Meta:
        Options.unique_together =  ('id_drive','owner')

    def __unicode__(self):
        return self.name + " (" + str(self.owner) + ")"

class SharedSecretFile(models.Model):
    """ model to share files between users"""

    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=256)

    iv = models.CharField(max_length=30)

    key = models.CharField(max_length=350)

    ct = models.TextField()

    creator = models.ForeignKey('sirs_users.CustomUser', related_name = 'publisher')
    
    destiny_user = models.ForeignKey('sirs_users.CustomUser', related_name = 'consumer')


    class Meta:
        Options.unique_together = ('id','creator')

    def __unicode__(self):
        return self.name + " (" + str(self.owner) + ")"