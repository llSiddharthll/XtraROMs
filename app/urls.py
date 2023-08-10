from django.urls import path 
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('custom_roms/', views.custom_roms, name="custom_roms"),
    path('magisk_modules/', views.magisk_modules, name ="magisk_modules"),
    path('comment/',views.comment,name='comment'),
    path('search-roms/', search_roms, name='search_roms'),
    path('search-mods/', search_mods, name='search_mods'),
    path('manage_user_profiles/', views.manage_user_profiles, name='manage_user_profiles'),
    path('update_user_profile/<int:profile_id>/', views.update_user_profile, name='update_user_profile'),
]