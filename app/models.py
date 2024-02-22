from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model

class CustomROM(models.Model):
    name = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    credits = models.CharField(null=True, max_length=50)
    image = models.ImageField(upload_to="images")
    link = models.URLField(max_length=225)
    details = models.TextField()
    upload_date = models.DateField(null=True, blank=True) # use auto_now instead of auto_now_add
    boot_link = models.URLField(max_length=225, null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_roms',default=0)


    def __str__(self):
        return self.name
    

class CustomMOD(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    credits = models.CharField(null=True, max_length=50)
    link = models.URLField()
    details = models.TextField()
    upload_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_mods',default=0)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_authorized = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_picture/", null=True, blank=True)
    status_choices = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("away", "Away"),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default="offline")
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class Message(models.Model):       
    content = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length = 20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('timestamp',)
        
        
class Friendship(models.Model):
    status_choices = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("blocked", "Blocked"),
    ]
    user1 = models.ForeignKey(UserProfile, related_name="friendships_initiated", on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile, related_name="friendships_received", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default="pending")
    conversation = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user1.user.username} and {self.user2.user.username}" #type:ignore

class OnlineStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def mark_online(self):
        self.is_online = True
        self.save(update_fields=['is_online'])

    def mark_offline(self):
        self.is_online = False
        self.save(update_fields=['is_online'])


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = [('can_change_permission', 'Can Change Permissions')] 

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set'  
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set' 
    )

    def __str__(self):
        return self.username  
