from django.db import models
from django.contrib.auth.models import User

class CustomROM(models.Model):

    name = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    credits = models.CharField(null=True, max_length=50)
    image = models.ImageField(upload_to="images")
    link = models.URLField(max_length=225)
    details = models.TextField()

    def __str__(self):
        return self.name
    
    
class CustomMOD(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    credits = models.CharField(null=True, max_length=50)
    link = models.URLField()
    details = models.TextField()

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_authorized = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name == None:
            return "ERROR-CUSTOMER NAME IS NULL"
        return self.name
