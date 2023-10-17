from django import forms
from .models import *

class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Change to CustomUser
        fields = ['username']

class UploadROMForm(forms.ModelForm):
    DEVICE_CHOICES = [
        ("Fleur / Miel", "Fleur / Miel"),
        ("Viva / Vida", "Viva / Vida"),
        ("Ocean / Sea", "Ocean / Sea"),
        ("Blossom", "Blossom"),
        ("Lavander", "Lavander"),
        ("Ginkgo / Willow", "Ginkgo / Willow"),
        ("X01BD", "X01BD"),
        ("Vince", "Vince"),
        ("Ruby / Rubypro", "Ruby / Rubypro")
    ]

    device = forms.ChoiceField(choices=DEVICE_CHOICES)

    class Meta:
        model = CustomROM
        fields = ('name', 'device', 'credits', 'image', 'link', 'boot_link', 'details', 'upload_date')
        widgets = {
            'upload_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UploadMODForm(forms.ModelForm):
    class Meta:
        model = CustomMOD
        fields = ('name', 'image', 'credits', 'link', 'details', 'upload_date')
        widgets = {
            'upload_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
