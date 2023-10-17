from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from allauth.account.views import SignupView, LoginView


class CustomSignupView(SignupView):
    def form_valid(self, form):
        try:
            # Call the parent class's form_valid method to create the user
            response = super().form_valid(form)

            # Set the authentication backend
            self.user.backend = "django.contrib.auth.backends.ModelBackend"
            self.user.save()

            # Create UserProfile
            user_profile = UserProfile.objects.create(
                user=self.user,
                # Add other fields as needed
            )

            # Log the user in
            login(self.request, self.user)

            print("UserProfile created:", user_profile)

            return response

        except Exception as e:
            print("Error creating UserProfile:", str(e))


class CustomLoginView(LoginView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def edit_rom(request, rom_id):
    rom = get_object_or_404(CustomROM, id=rom_id)

    if request.method == "POST":
        edit_form = UploadROMForm(request.POST, request.FILES, instance=rom)
        if edit_form.is_valid():
            new_image = edit_form.cleaned_data["image"]
            edit_form.image = new_image  # type: ignore
            edit_form.save()  # Handle image update and upload date retention
            return redirect("custom_roms")  # Successful, redirect back to ROM listing
    else:
        edit_form = UploadROMForm(instance=rom)

    context = {"edit_form": edit_form, "rom": rom, "rom_id": rom_id}
    return render(request, "edit_form.html", context)


def edit_mod(request, mod_id):
    mod = get_object_or_404(CustomMOD, id=mod_id)
    edit_form = UploadMODForm(instance=mod)

    if request.method == "POST":
        edit_form = UploadMODForm(request.POST, request.FILES, instance=mod)
        if edit_form.is_valid():
            edit_form.save()
            return redirect("magisk_modules")  # Successful, no content

    context = {"edit_form": edit_form, "mod": mod, "mod_id": mod_id}
    return render(request, "edit_mod.html", context)


def search_custom_roms(request):
    query = request.GET.get("q", "")
    if query:
        filtered_roms = CustomROM.objects.filter(
            Q(name__icontains=query)
            | Q(device__icontains=query)  # Search by name
            | Q(credits__icontains=query)  # Search by device  # Search by credits
        )

        roms_data = []
        for rom in filtered_roms:
            likes_count = rom.likes.count()
            rom_data = {
                "id": rom.id,  # type: ignore
                "name": rom.name,
                "device": rom.device,
                "details": rom.details,
                "link": rom.link,
                "credits": rom.credits,
                "upload_date": rom.upload_date,
                "likes": likes_count,
                "image_url": rom.image.url,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            roms_data.append(rom_data)
    else:
        roms_data = []

    return JsonResponse({"results": roms_data})


def search_custom_mods(request):
    query = request.GET.get("q", "")
    if query:
        filtered_mods = CustomMOD.objects.filter(
            Q(name__icontains=query)
            | Q(credits__icontains=query)  # Search by name  # Search by credits
        )

        mods_data = []
        for mod in filtered_mods:
            likes_count = mod.likes.count()
            mod_data = {
                "id": mod.id,  # type: ignore
                "name": mod.name,
                "details": mod.details,
                "link": mod.link,
                "credits": mod.credits,
                "upload_date": mod.upload_date,
                "likes": likes_count,
                "image_url": mod.image.url,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            mods_data.append(mod_data)
    else:
        mods_data = []

    return JsonResponse({"results": mods_data})


def home(request):
    total_users = User.objects.count()
    total_roms = CustomROM.objects.count()
    total_mods = CustomMOD.objects.count()
    total_items = total_roms + total_mods
    roms = CustomROM.objects.all()
    mods = CustomMOD.objects.all()
    context={
        "roms": roms, 
        "mods": mods,
        "total_users": total_users,
        "total_items":total_items,
    }
    return render(request, "home.html", context)
    # Handle the case when the user is not authenticated


def logout_request(request):
    logout(request)
    return redirect("/")


@csrf_exempt
@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user = request.user

    if request.method == "POST":
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES)
        update_username_form = UpdateUsernameForm(request.POST, instance=user)

        rom_form = UploadROMForm(request.POST, request.FILES)
        if rom_form.is_valid():
            rom = rom_form.save()
            rom.uploaded_by = request.user
            rom.save()
            return redirect("custom_roms")  # Redirect back to the same page

        mod_form = UploadMODForm(request.POST, request.FILES)
        if mod_form.is_valid():
            mod = mod_form.save()
            mod.uploaded_by = request.user
            mod.save()
            return redirect("magisk_modules")  # Redirect back to the same page

        if update_username_form.is_valid():
            update_username_form.save()

        if profile_picture_form.is_valid():
            new_image = profile_picture_form.cleaned_data["profile_picture"]
            user_profile.profile_picture = new_image
            user_profile.save()

            return redirect("profile")
    else:
        profile_picture_form = ProfilePictureForm(instance=user_profile)
        update_username_form = UpdateUsernameForm(instance=user)

    is_validated = ""
    if user_profile.is_authorized:
        is_validated = "Yes"
    else:
        is_validated = "No"
    context = {
        "user_profile": user_profile,
        "is_validated": is_validated,
        "profile_picture_form": profile_picture_form,
        "update_username_form": update_username_form,
    }

    return render(request, "profile.html", context)


def custom_roms(request):
    roms = CustomROM.objects.all().order_by("-upload_date")
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == "POST":
            form = UploadROMForm(request.POST, request.FILES)
            if form.is_valid():
                rom = form.save()
                rom.uploaded_by = request.user
                rom.save()
                return redirect("custom_roms")  # Redirect back to the same page

            # Handle like action

            rom_id = request.POST.get("rom_id")
            if rom_id:
                rom = CustomROM.objects.get(pk=rom_id)
                user_liked = rom.likes.filter(id=request.user.id).exists()

                if user_liked:
                    rom.likes.remove(request.user)
                else:
                    rom.likes.add(request.user)

                return JsonResponse({"likes": rom.likes.count()})

        else:
            form = UploadROMForm()

        # Format description for each ROM
        for rom in roms:
            rom.formatted_details = mark_safe(  # type: ignore
                rom.details.replace("\n", "<br>").replace("-", "&#8226;")
            )
            rom.save()
        return render(
            request,
            "custom_roms.html",
            {"roms": roms, "user_profile": user_profile, "form": form},
        )

    return render(request, "custom_roms.html", {"roms": roms})


def rom_details(request, rom_id):
    rom = get_object_or_404(CustomROM, id=rom_id)
    rom_id = request.POST.get("rom_id")
    if rom_id:
        rom = CustomROM.objects.get(pk=rom_id)
        user_liked = rom.likes.filter(id=request.user.id).exists()

        if user_liked:
            rom.likes.remove(request.user)
        else:
            rom.likes.add(request.user)

        return JsonResponse({"likes": rom.likes.count()})
    formatted_details = mark_safe(
        rom.details.replace("\n", "<br>").replace("-", "&#8226;")
    )
    return render(
        request,
        "rom_details.html",
        {"rom": rom, "formatted_details": formatted_details},
    )


def mod_details(request, mod_id):
    mod = get_object_or_404(CustomMOD, id=mod_id)
    mod_id = request.POST.get("mod_id")
    if mod_id:
        mod = CustomMOD.objects.get(pk=mod_id)
        user_liked = mod.likes.filter(id=request.user.id).exists()

        if user_liked:
            mod.likes.remove(request.user)
        else:
            mod.likes.add(request.user)

        return JsonResponse({"likes": mod.likes.count()})
    formatted_details = mark_safe(
        mod.details.replace("\n", "<br>").replace("-", "&#8226;")
    )
    return render(
        request,
        "mod_details.html",
        {"mod": mod, "formatted_details": formatted_details},
    )


def magisk_modules(request):
    mods = CustomMOD.objects.all().order_by("-upload_date")
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

        if request.method == "POST":
            form = UploadMODForm(request.POST, request.FILES)
            if form.is_valid():
                mod = form.save()
                mod.uploaded_by = request.user
                mod.save()
                return redirect("magisk_modules")  # Redirect back to the same page

            # Handle like action

            mod_id = request.POST.get("mod_id")
            if mod_id:
                mod = CustomMOD.objects.get(pk=mod_id)
                user_liked = mod.likes.filter(id=request.user.id).exists()

                if user_liked:
                    mod.likes.remove(request.user)
                else:
                    mod.likes.add(request.user)

                return JsonResponse({"likes": mod.likes.count()})

        else:
            form = UploadMODForm()

        # Format description for each mod
        for mod in mods:
            mod.formatted_details = mark_safe(  # type: ignore
                mod.details.replace("\n", "<br>").replace("-", "&#8226;")
            )

        return render(
            request,
            "magisk_modules.html",
            {"mods": mods, "user_profile": user_profile, "form": form},
        )

    return render(request, "magisk_modules.html", {"mods": mods})


@login_required
@staff_member_required
def manage_user_profiles(request):
    profiles = UserProfile.objects.all()
    return render(
        request, "app_userprofile/manage_user_profiles.html", {"profiles": profiles}
    )


@login_required
def update_user_profile(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)

    if request.method == "POST":
        is_authorized = request.POST.get("is_authorized")
        profile.is_authorized = is_authorized == "on"
        profile.save()
        return redirect("manage_user_profiles")

    return render(
        request, "app_userprofile/update_user_profile.html", {"profile": profile}
    )


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def comment_policy_view(request):
    return render(request, "comment_policy.html")


import json


def blog(request):
    try:
        # Specify the encoding as 'utf-8-sig' to handle common Unicode issues
        with open(
            "app/saved_templates/all_articles.json", "r", encoding="utf-8-sig"
        ) as json_file:
            articles = json.load(json_file)
    except Exception as e:
        # Handle any exceptions that might occur when reading the JSON file
        # You can log the error or take other appropriate actions here.
        print(f"Error reading JSON file: {str(e)}")
        articles = (
            []
        )  # Set articles to an empty list to avoid issues if the file can't be read
    return render(request, "blog.html", {"articles": articles})


import openai

# Set your OpenAI API key
openai.api_key = "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"


# Create a function that handles the chat interaction
def chat_with_openai(messages):
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return chat.choices[0].message.content  # type: ignore


# Create a Django view that handles the chat interactions
@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        # Extract the user's message from the POST request
        user_message = request.POST.get("message", "")

        # Define the initial system message
        messages = [{"role": "system", "content": "You are an intelligent assistant."}]

        # Append the user's message to the message history
        if user_message:
            messages.append({"role": "user", "content": user_message})

        # Get a response from OpenAI
        assistant_response = chat_with_openai(messages)

        # Append the assistant's response to the message history
        messages.append({"role": "assistant", "content": assistant_response})

        # Return the assistant's response as JSON
        return JsonResponse({"response": assistant_response})

    else:
        return JsonResponse({"error": "Invalid request method. Use POST."})
