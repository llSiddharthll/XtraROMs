from django.urls import path
from .views import *
from . import fbv

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/signup/", SignupView.as_view(), name="signup"),
    path("account/login/", LoginView.as_view(), name="login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("custom_roms/", RomsView.as_view(), name="roms"),
    path("magisk_modules/", ModsView.as_view(), name="mods"),
    path("privacy_policy", PolicyView.as_view(), name="policy"),
    path('rom_detail/<slug:slug>/', ROMDetailsView.as_view(), name='rom_details'),
    path("search_roms/", fbv.search_roms, name="search_roms"),
    path('mod_detail/<slug:slug>/', MODDetailsView.as_view(), name='mod_details'),
    path("search_mods/", fbv.search_mods, name="search_mods"),
    path('edit_rom/<slug:slug>/', fbv.edit_rom, name='edit_rom'),
    path('edit_mod/<slug:slug>/', fbv.edit_mod, name='edit_mod'),
    path('upload_roms', fbv.upload_roms, name="upload_roms"),
    path('upload_mods', fbv.upload_mods, name="upload_mods"),
    path('manage_users/', ManageUserView.as_view(), name='manage_users'),
    path('xtraknowledge/', XtraKnowledgeView.as_view(), name='xtraknowledge')
]