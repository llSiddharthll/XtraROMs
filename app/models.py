from django.db import models
from django.contrib.auth.models import User
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
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True)
    is_authorized = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    # Add other fields as needed

    def __str__(self):
        return str(self.user)

class ScrapData(models.Model):
    url = models.URLField()
    image_url = models.URLField()
    article_id = models.CharField(max_length=255)
    article_title = models.CharField(max_length=255)
    article_content = models.TextField()

    def __str__(self):
        return self.article_id


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    
    class Meta:
        permissions = [('can_change_permission', 'Can Change Permissions')]  # Example custom permission
    
    # Add any other fields or methods you need for your custom user model

    # Specify unique related_name values for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set'  # Unique related_name for groups
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set'  # Unique related_name for user_permissions
    )

    def __str__(self):
        return self.username  # You can choose a different field for the string representation


