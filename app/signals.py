# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=SocialAccount)
def update_user_profile(sender, instance, created, **kwargs):
    if created and instance.provider == 'google':
        user_profile = UserProfile.objects.get(user=instance.user)
        user_profile.google_username = instance.extra_data.get('name', '')
        user_profile.save()

        # Update the email as well
        user = instance.user
        user.email = instance.extra_data.get('email', '')
        user.save()
