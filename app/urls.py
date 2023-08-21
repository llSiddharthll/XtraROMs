from django.urls import path, include
from . import views
from .views import *
from allauth.socialaccount import views as socialaccount_views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('custom_roms/', views.custom_roms, name='custom_roms'),
    path('edit_rom/<int:rom_id>/', views.edit_rom, name='edit_rom'),
    path('edit_mod/<int:mod_id>/', views.edit_mod, name='edit_mod'),
    path('magisk_modules/', views.magisk_modules, name='magisk_modules'),
    path('comment/', views.comment, name='comment'),
    path('search/', search_custom_roms, name='search_custom_roms'),
    path('search-mods/', search_mods, name='search_mods'),
    path('manage_user_profiles/', views.manage_user_profiles, name='manage_user_profiles'),
    path('update_user_profile/<int:profile_id>/', views.update_user_profile, name='update_user_profile'),
    path('set-cookie/<str:interaction_data>/', views.set_cookie, name='set_cookie'),
    path('read-cookie/', views.read_cookie, name='read_cookie'),
    path('track-session/', views.track_session, name='track_session'),
    path('accounts/', include('allauth.account.urls')),
    path('socialaccounts/', include('allauth.socialaccount.urls')),
    path('custom_roms/results', views.results_template, name='results_template'),
]
