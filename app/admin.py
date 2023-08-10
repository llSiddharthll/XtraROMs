from django.contrib import admin
from .models import *

# Register your models here.
class CustomROMs(admin.ModelAdmin):
    list_display=('name', 'device')
admin.site.register(CustomROM,CustomROMs)

class CustomMODs(admin.ModelAdmin):
    list_display=('name',)
admin.site.register(CustomMOD,CustomMODs)

class UserProfiles(admin.ModelAdmin):
    list_display=('user',)
admin.site.register(UserProfile,UserProfiles)

class Contacts(admin.ModelAdmin):
    list_display=('name',)
admin.site.register(Contact,Contacts)

class Comments(admin.ModelAdmin):
    list_display=('name',)
admin.site.register(Comment,Comments)