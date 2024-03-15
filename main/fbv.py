from .models import CustomROM, CustomMOD
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .forms import *
from django.shortcuts import redirect, get_object_or_404, render

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
    if request.method == "POST":
        try:
            name = request.POST.get("rom_name")
            device = request.POST.get("rom_device")
            credits_name = request.POST.get("rom_credits")
            credits, created = Credits.objects.get_or_create(name=credits_name)
            image = request.FILES.get("rom_image")
            link = request.POST.get("rom_link")
            details = request.POST.get("rom_details")
            
            # Ensure all required fields are provided before creating the ROM object
            if name and device and credits_name and image and link and details:
                # Create a CustomROM instance
                rom = CustomROM(
                    name=name,
                    device=device,
                    credits=credits,
                    image=image,
                    link=link,
                    details=details,
                    uploaded_by=request.user
                )
                # Save the instance to generate the slug automatically
                rom.save()
                return redirect("roms")  # Redirect to ROMs page after successful upload
            else:
                # Handle the case when required fields are missing
                error_message = "Please fill in all required fields."
                return HttpResponse(error_message)  # Return error message with status code 400 (Bad Request)
        
        except Exception as e:
            # Handle any other exceptions that might occur
            error_message = str(e)  # Convert the exception to a string for better error reporting
            return HttpResponse(error_message)
        
def upload_mods(request):
    if request.method == "POST":
        try:
            name = request.POST.get("mod_name")
            device = request.POST.get("mod_device")
            credits_name = request.POST.get("mod_credits")
            credits, created = Credits.objects.get_or_create(name=credits_name)
            image = request.FILES.get("mod_image")
            link = request.POST.get("mod_link")
            details = request.POST.get("mod_details")
            
            # Ensure all required fields are provided before creating the ROM object
            if name and device and credits_name and image and link and details:
                # Create a CustomROM instance
                mod = CustomMOD(
                    name=name,
                    device=device,
                    credits=credits,
                    image=image,
                    link=link,
                    details=details,
                    uploaded_by=request.user
                )
                # Save the instance to generate the slug automatically
                mod.save()
                return redirect("mods")  # Redirect to ROMs page after successful upload
            else:
                # Handle the case when required fields are missing
                error_message = "Please fill in all required fields."
                return JsonResponse({"error": error_message}, status=400)  # Return error message with status code 400 (Bad Request)
        
        except Exception as e:
            # Handle any other exceptions that might occur
            error_message = str(e)  # Convert the exception to a string for better error reporting
            return JsonResponse({"error": error_message}, status=500)