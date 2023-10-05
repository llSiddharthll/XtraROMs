from django.urls import path, include, re_path
from . import views
from .views import *
from allauth.account.views import LoginView,ConfirmEmailView

appname = 'app'
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', CustomSignupView.as_view(), name='custom_signup'),
    path('accounts/login/', CustomLoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('custom_roms/', views.custom_roms, name='custom_roms'),
    path('rom_detail/rom_details_<int:rom_id>/', views.rom_details, name='rom_details'),
    path('mod_detail/mod_details_<int:mod_id>/', views.mod_details, name='mod_details'),
    path('edit_rom/editing_rom_<int:rom_id>/', views.edit_rom, name='edit_rom'),
    path('edit_mod/editing_mod_<int:mod_id>/', views.edit_mod, name='edit_mod'),
    path('magisk_modules/', views.magisk_modules, name='magisk_modules'),
    path('search/', views.search_custom_roms, name='search_custom_roms'),
    path('search-mods/', views.search_custom_mods, name='search_custom_mods'),
    path('manage_user_profiles/', views.manage_user_profiles, name='manage_user_profiles'),
    path('update_user_profile/<int:profile_id>/', views.update_user_profile, name='update_user_profile'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('chat-view/', views.chat_view, name='chat-view'),
    path('blog/', views.blog, name='blog'),
    path('chatbot/comment-policy/', views.comment_policy_view, name='comment-policy'),
]
