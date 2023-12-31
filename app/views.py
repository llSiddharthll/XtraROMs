from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
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
from .consumers import *

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'

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
    template_name = 'account/login.html'

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
            | Q(credits__icontains=query)
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
    context = {
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
            rom.formatted_details = mark_safe(# type: ignore
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
                return redirect("magisk_modules")  

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
            mod.formatted_details = mark_safe(# type: ignore
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


@login_required
def friends(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    # Assuming UserProfile has a ForeignKey to User with the related_name 'user_profile'
    try:
        user_profile = request.user.userprofile  # Use 'userprofile' instead of 'user_profile'
    except UserProfile.DoesNotExist:
        user_profile = None

    if not user_profile:
        # Handle the case where the user does not have a UserProfile
        return HttpResponse("User profile not found")

    # Filter accepted friend relationships for the current user
    user_friends = Friendship.objects.filter(
        (models.Q(user1=user_profile) | models.Q(user2=user_profile)), status='accepted'
    )

    # Filter pending friend requests for the current user
    friend_requests = Friendship.objects.filter(user2=user_profile, status='pending')

    # Exclude current friends and pending friend requests
    exclude_users = [
        friend.user1.user for friend in user_friends
    ] + [
        friend.user2.user for friend in user_friends
    ] + [
        request.user  # Assuming request.user is a User instance
    ]  # type:ignore

    # Get all users excluding the current user and their friends
    all_users = UserProfile.objects.exclude(user__in=[user for user in exclude_users]).exclude(user=request.user)  # type:ignore
    context = {
        'user_friends': user_friends,
        'friend_requests': friend_requests,
        'all_users': all_users,
    }

    return render(request, 'Friends.html', context)


@login_required
def friend_profile(request, friend_username):
    friend = get_object_or_404(User, username=friend_username)
    
    # You can access friend data here and pass it to the template
    # For example, if User model has a field named 'email', you can do:
    friend_email = friend.email

    context = {
        'friend': friend,
        'friend_email': friend_email,
        # Add other friend data as needed
    }

    return render(request, 'FriendProfile.html', context)

def chat(request, friendship_id):
    friends = get_object_or_404(Friendship, id=friendship_id)
    user = request.user

    # Use tuple unpacking with get_or_create
    online_status, created = OnlineStatus.objects.get_or_create(user=user)
    
    user_profile = UserProfile.objects.get(user=request.user)

    # Pass online_status, friends, messages, and conversation_id to the template
    return render(request, 'chat.html', {'online_status': online_status, 'friends': [friends], 'user_profile':user_profile})



@login_required
def send_friend_request(request, username):
    user_to_add = get_object_or_404(User, username=username)

    # Ensure that UserProfile instances are used for the friendship relationship
    user_profile = UserProfile.objects.get(user=request.user)
    user_to_add_profile = UserProfile.objects.get(user=user_to_add)

    # Check if a friendship already exists
    existing_friendship = Friendship.objects.filter(
        (models.Q(user1=user_profile, user2=user_to_add_profile) | models.Q(user1=user_to_add_profile, user2=user_profile)),
        status='accepted'
    ).exists()

    if not existing_friendship:
        # Create a new friendship request
        Friendship.objects.create(user1=user_profile, user2=user_to_add_profile, status='pending')
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Friendship already exists.'})


@login_required
def accept_friend_request(request, friendship_id):
    user_profile = UserProfile.objects.get(user=request.user)
    friendship = get_object_or_404(Friendship, id=friendship_id, user2=user_profile, status='pending')
    friendship.status = 'accepted'
    friendship.save()
    return JsonResponse({'status': 'success'})

@login_required
def reject_friend_request(request, friendship_id):
    user_profile = UserProfile.objects.get(user=request.user)
    friendship = get_object_or_404(Friendship, id=friendship_id, user2=user_profile, status='pending')
    friendship.status = 'rejected'
    friendship.save()
    return JsonResponse({'status': 'success'})
