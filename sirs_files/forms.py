from django.forms import ModelForm, Textarea, TextInput, FileField, CharField, HiddenInput, Form, ChoiceField
from .models import SecretFile, SharedSecretFile
from django import forms


class FileUpload(ModelForm):
    """FileUpload form represents the form to upload a file
    Uses the fields on the SecretFile model and adds a filefield,
    which should NOT be upload. Objective is to cipher on the client
    side and just upload the file name, IV, key and ciphertext
    """
    file = FileField(label='File to cipher', required=False)
    pubKey = CharField(widget=HiddenInput())

    class Meta:
        model = SecretFile
        fields = ['name', 'iv', 'key', 'ct', 'file', 'pubKey']
        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'iv': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'key': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'ct': Textarea(attrs={'readonly': 'readonly'})
        }


class FileDownload(ModelForm):
    """FileDownload forms represents the form to download a file
    Maps the fields on the SecretFile model to the form.
    """

    privKey = FileField(label='Private Key (PEM)', required=False)

    class Meta:
        model = SecretFile
        fields = ['name', 'iv', 'key', 'ct']
        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'iv': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'key': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'ct': Textarea(attrs={'readonly': 'readonly'})
        }

class FileShare(ModelForm):
    """ FileShare form represents the form to share a file with another user
    Maps the fields on the SharedSecretFile model to the form (the ones needed at least).
    """
    
    pubKey = CharField(widget=HiddenInput())
    privKey = FileField(label='Private Key (PEM)', required = False)
    username = CharField(widget=HiddenInput(), required = False)
    class Meta:
        model = SharedSecretFile
        
        fields = ['name','iv','key','ct']
        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'iv': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
             'key': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'ct': Textarea(attrs={'readonly': 'readonly'}),
        }

class FileAndUserSelection(Form):

    def __init__(self,options, *args, **kwargs):
        super(FileAndUserSelection, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.ChoiceField(choices = options)
        self.fields['username'] = CharField(max_length=30,min_length = 1)
        
    
        
