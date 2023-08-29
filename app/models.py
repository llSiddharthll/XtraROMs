from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class CustomROM(models.Model):
    name = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    credits = models.CharField(null=True, max_length=50)
    image = CloudinaryField("images")
    link = models.URLField(max_length=225)
    details = models.TextField()
    upload_date = models.DateField(null=True, blank=True) # use auto_now instead of auto_now_add
    boot_link = models.URLField(max_length=225, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_roms',default=0)


    def __str__(self):
        return self.name
    
    
class CustomMOD(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField("images")
    credits = models.CharField(null=True, max_length=50)
    link = models.URLField()
    details = models.TextField()
    upload_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_mods',default=0)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_authorized = models.BooleanField(default=False)
    profile_picture = CloudinaryField('profile_pictures', blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.user.username

class UserCookie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interaction_data = models.TextField(default="")

    def __str__(self):
        return f"{self.user.username} - Cookie"