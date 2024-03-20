from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class UploadROMForm(forms.ModelForm):

    credits = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter a name or select from existing",
                "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
            }
        ),
        label="Credits",
    )

    class Meta:
        model = CustomROM
        fields = ["name", "device", "credits", "image", "link", "details"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "CrDroid/Lineage",
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "device": forms.TextInput(
                attrs={
                    "placeholder": "Ruby/Fleur",
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "placeholder": "ROM Image",
                    "class": "placeholder-[var(--text-500)] mt-1 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "link": forms.URLInput(
                attrs={
                    "placeholder": "https://something/download",
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "details": forms.Textarea(
                attrs={
                    "placeholder": "Provide changelogs, flashing details, must provide issues or bugs if any",
                    "rows": 3,
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
        }

    def clean_credits(self):
        credit_name = self.cleaned_data['credits']

        # Check if a Credits instance with the given name already exists
        credit_instance, created = Credits.objects.get_or_create(name=credit_name)

        return credit_instance

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.credits = self.cleaned_data['credits']
        if commit:
            instance.save()
        return instance


class UploadMODForm(forms.ModelForm):

    credits = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "JohnDoe",
                "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
            }
        ),
        label="Credits",
    )

    class Meta:
        model = CustomMOD
        fields = ["name", "credits", "image", "link", "details"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "MiFlash/Magisk Module",
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "placeholder": "Image",
                    "class": "placeholder-[var(--text-500)] mt-1 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "link": forms.URLInput(
                attrs={
                    "placeholder": "https://something/download",
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
            "details": forms.Textarea(
                attrs={
                    "placeholder": "Provide changelogs, details, features, use cases etc.",
                    "rows": 3,
                    "class": "placeholder-[var(--text-500)] mt-1 p-2 border border-gray-300 rounded-md w-full bg-[var(--text-800)] text-[var(--text-200)]"
                }
            ),
        }

    def clean_credits(self):
        credit_name = self.cleaned_data['credits']

        # Check if a Credits instance with the given name already exists
        credit_instance, created = Credits.objects.get_or_create(name=credit_name)

        return credit_instance

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.credits = self.cleaned_data['credits']
        if commit:
            instance.save()
        return instance


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=150, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'profile_picture']
        

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        user_profile = super(UserProfileForm, self).save(commit=False)
        user = user_profile.user

        # Update user fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']

        # Save user and user_profile
        if commit:
            user.save()
            user_profile.save()

        return user_profile