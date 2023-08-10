from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe
from django.http import JsonResponse


# Create your views here.


def search_roms(request):
    query = request.GET.get('query', '').lower().strip()

    filtered_roms = CustomROM.objects.filter(name__icontains=query)
    
    roms_data = []
    for rom in filtered_roms:
        rom_data = {
            'name': rom.name,
            'device': rom.device,
            'details': rom.details,
            'link': rom.link,
            'image_url': rom.image.url,
        }
        roms_data.append(rom_data)
    
    return JsonResponse({'roms': roms_data})

def search_mods(request):
    query = request.GET.get('query', '').lower().strip()

    filtered_mods = CustomMOD.objects.filter(name__icontains=query)
    
    mods_data = []
    for mod in filtered_mods:
        mod_data = {
            'name': mod.name,
            'device': mod.device,
            'details': mod.details,
            'link': mod.link,
            'image_url': mod.image.url,
        }
        mods_data.append(mod_data)
    
    return JsonResponse({'roms': mods_data})


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Add any additional logic or notifications here
            return redirect("home")  # Redirect to the same page after submission
    else:
        form = ContactForm()
    return render(request, "home.html", {"form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="app_userprofile/login.html", context={"form": form})

def logout_request(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a UserProfile instance for the new user
            UserProfile.objects.create(user=user)

            # Log the user in after registration
            login(request, user)
            return redirect('home')  # Redirect to the home page or a different URL
    else:
        form = SignUpForm()
    return render(request, 'app_userprofile/signup.html', {'form': form})


from django.utils.safestring import mark_safe

def custom_roms(request):
    roms = CustomROM.objects.all()

    if request.method == 'POST':
        form = UploadROMForm(request.POST, request.FILES)
        if form.is_valid():
            rom = form.save(commit=False)
            rom.uploaded_by = request.user
            rom.save()
            return redirect('custom_roms')  # Redirect back to the same page

    else:
        form = UploadROMForm()

    # Format description for each ROM
    for rom in roms:
        rom.formatted_details = mark_safe(rom.details.replace("\n", "<br>").replace("-", "&#8226;"))

    return render(request, 'custom_roms.html', {'roms': roms, 'form': form})



def magisk_modules(request):
    mods = CustomMOD.objects.all()

    if request.method == 'POST':
        form = UploadMODForm(request.POST, request.FILES)
        if form.is_valid():
            mod = form.save(commit=False)
            mod.uploaded_by = request.user
            mod.save()
            return redirect('magisk_modules')  # Redirect back to the same page

    else:
        form = UploadMODForm()

    # Format description for each ROM
    for mod in mods:
        mod.formatted_details = mark_safe(mod.details.replace("\n", "<br>").replace("-", "&#8226;"))

    return render(request, 'magisk_modules.html', {'mods': mods, 'form': form})

@login_required
@staff_member_required
def manage_user_profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'app_userprofile/manage_user_profiles.html', {'profiles': profiles})

@login_required
@staff_member_required
def update_user_profile(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)
    
    if request.method == 'POST':
        is_authorized = request.POST.get('is_authorized')
        profile.is_authorized = is_authorized == 'on'
        profile.save()
        return redirect('manage_user_profiles')
    
    return render(request, 'app_userprofile/update_user_profile.html', {'profile': profile})


def comment(request):

    if request.method == "POST":
        n = request.POST.get('Name')
        mess = request.POST.get('Message')
        e = Comment.objects.create(name=n, message=mess)
        e.save()
        return redirect('/comment/')

    data = Comment.objects.all().values()
    return render(request, 'comment.html', {'data': data})