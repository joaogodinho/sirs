from django.forms import ModelForm, Textarea, TextInput, FileField
from .models import SecretFile


class FileUpload(ModelForm):
    """FileUpload form represents the form to upload a file
    Uses the fields on the SecretFile model and adds a filefield,
    which should NOT be upload. Objetive is to cipher on the client
    side and just upload the file name, IV, key and ciphertext
    """
    file = FileField(label='File to cipher', required=False)

    class Meta:
        model = SecretFile
        fields = ['name', 'iv', 'key', 'ct']
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
    class Meta:
        model = SecretFile
        fields = ['name', 'iv', 'key', 'ct']
        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'iv': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'key': TextInput(attrs={'readonly': 'readonly', 'size': 50}),
            'ct': Textarea(attrs={'readonly': 'readonly'})
        }
