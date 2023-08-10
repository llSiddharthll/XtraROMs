from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UploadROMForm(forms.ModelForm):
    class Meta:
        model = CustomROM
        fields = ('name','device','image','link','details')

class UploadMODForm(forms.ModelForm):
    class Meta:
        model = CustomMOD
        fields = ('name','image','link','details')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),  # Adjust the rows value as needed
        }
