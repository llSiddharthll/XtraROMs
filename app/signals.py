from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OnlineStatus
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_online_status(sender, instance, created, **kwargs):
    if created:
        OnlineStatus.objects.create(user=instance)
