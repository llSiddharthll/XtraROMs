from .models import CustomROM, CustomMOD
from django.db.models import Q
from django.http import JsonResponse, HttpResponseServerError
from .forms import *
from django.shortcuts import redirect, get_object_or_404, render
import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def search_roms(request):
    query = request.GET.get("q", "")
    if query:
        filtered_roms = CustomROM.objects.filter(
            Q(name__icontains=query)
            | Q(device__icontains=query)
        )

        roms_data = []
        for rom in filtered_roms:
            likes_count = rom.likes.count()
            comments_count = rom.comments.count()
            rom_data = {
                "id": rom.id,
                "name": rom.name,
                "device": rom.device,
                "details": rom.details,
                "link": rom.link,
                "upload_date": rom.upload_date,
                "image_url": rom.image.url,
                "likes": likes_count,
                "credits": rom.credits.name if rom.credits else None,
                "slug": rom.slug,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            roms_data.append(rom_data)
    else:
        roms_data = []

    return JsonResponse({"results": roms_data})

def search_mods(request):
    query = request.GET.get("q", "")
    if query:
        filtered_mods = CustomMOD.objects.filter(
            Q(name__icontains=query)
        )

        mods_data = []
        for mod in filtered_mods:
            likes_count = mod.likes.count()
            mod_data = {
                "id": mod.id,
                "name": mod.name,
                "details": mod.details,
                "link": mod.link,
                "upload_date": mod.upload_date,
                "image_url": mod.image.url,
                "likes": likes_count,
                "credits": mod.credits.name if mod.credits else None,
                "slug": mod.slug,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            mods_data.append(mod_data)
    else:
        mods_data = []

    return JsonResponse({"results": mods_data})


def edit_rom(request, slug):
    rom = get_object_or_404(CustomROM, slug=slug)

    if request.method == "POST":
        edit_form = UploadROMForm(request.POST, request.FILES, instance=rom)
        if edit_form.is_valid():
            new_image = edit_form.cleaned_data["image"]
            credits = edit_form.cleaned_data["credits"]
            edit_form.credits = credits
            edit_form.image = new_image 
            edit_form.save() 
            return redirect("roms") 
    else:
        edit_form = UploadROMForm(instance=rom)

    context = {"edit_form": edit_form, "rom": rom}
    return render(request, "edit_rom.html", context)


def edit_mod(request, slug):
    mod = get_object_or_404(CustomMOD, slug=slug)
    edit_form = UploadMODForm(instance=mod)

    if request.method == "POST":
        edit_form = UploadMODForm(request.POST, request.FILES, instance=mod)
        if edit_form.is_valid():
            new_image = edit_form.cleaned_data["image"]
            credits = edit_form.cleaned_data["credits"]
            edit_form.credits = credits
            edit_form.image = new_image 
            edit_form.save() 
            return redirect("mods") 

    context = {"edit_form": edit_form, "mod": mod}
    return render(request, "edit_mod.html", context)

def upload_roms(request):
    try:
        if request.method == 'POST':
            form = UploadROMForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('roms')  # Redirect to a success URL after saving
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"An error occurred: {e}")

    # If an error occurs or form is invalid, render the form again
    form = UploadROMForm()
    return render(request, 'dashboard.html', {'form': form})

def upload_mods(request):
    try:
        if request.method == 'POST':
            form = UploadMODForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('mods')  # Redirect to a success URL after saving
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"An error occurred: {e}")