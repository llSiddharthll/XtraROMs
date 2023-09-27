from django.contrib import admin
from .models import *

# Register your models here.
class CustomROMAdmin(admin.ModelAdmin):
    list_display = ('name', 'device', 'credits', 'upload_date')
    search_fields = ('name', 'device', 'credits')
admin.site.register(CustomROM, CustomROMAdmin)

class CustomMODAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits', 'upload_date')
    search_fields = ('name', 'credits')
admin.site.register(CustomMOD, CustomMODAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_authorized')
admin.site.register(UserProfile, UserProfileAdmin)

class ScrapDataAdmin(admin.ModelAdmin):
    list_display = ('article_id',)
admin.site.register(ScrapData, ScrapDataAdmin)
