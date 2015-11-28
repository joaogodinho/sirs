from django.forms import ModelForm, EmailField
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm as DjgoUserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(DjgoUserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserCustomCreationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['publicKey']
