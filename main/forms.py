from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username']

class UploadROMForm(forms.ModelForm):
    new_credits = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
        label='New Credits Name'
    )

    class Meta:
        model = CustomROM
        fields = ['name', 'device', 'credits', 'new_credits', 'image', 'link', 'details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'device': forms.TextInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'credits': forms.Select(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'image': forms.ClearableFileInput(attrs={'class': 'mt-1 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'link': forms.URLInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'details': forms.Textarea(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        credits = cleaned_data.get('credits')
        new_credits = cleaned_data.get('new_credits')

        if not credits and not new_credits:
            raise forms.ValidationError("Please select an existing credit or enter a new credit name.")

        return cleaned_data

    def save(self, commit=True):
        new_credits = self.cleaned_data.get('new_credits')
        if new_credits:
            credits, created = Credits.objects.get_or_create(name=new_credits)
            self.instance.credits = credits

        return super().save(commit)


class UploadMODForm(forms.ModelForm):
    new_credits = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
        label='New Credits Name'
    )

    class Meta:
        model = CustomMOD
        fields = ['name', 'credits', 'new_credits', 'image', 'link', 'details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'credits': forms.Select(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'image': forms.ClearableFileInput(attrs={'class': 'mt-1 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'link': forms.URLInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
            'details': forms.Textarea(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--secondary)] text-[var(--text)]'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        credits = cleaned_data.get('credits')
        new_credits = cleaned_data.get('new_credits')

        if not credits and not new_credits:
            raise forms.ValidationError("Please select an existing credit or enter a new credit name.")

        return cleaned_data

    def save(self, commit=True):
        new_credits = self.cleaned_data.get('new_credits')
        if new_credits:
            credits, created = Credits.objects.get_or_create(name=new_credits)
            self.instance.credits = credits

        return super().save(commit)



class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
