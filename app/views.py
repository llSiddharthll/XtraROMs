from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe
from django.http import JsonResponse
# app/views.py
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def set_cookie(request, interaction_data):
    response = HttpResponse("Cookie set!")
    # Append interaction data to the cookie value
    current_cookie_data = request.COOKIES.get("user_interactions", "")
    new_cookie_data = f"{current_cookie_data}|{interaction_data}"
    response.set_cookie("user_interactions", new_cookie_data, max_age=3600)
    return response

def read_cookie(request):
    user_interactions = request.COOKIES.get("user_interactions")
    return HttpResponse(f"User Interactions: {user_interactions}")

def track_session(request, obj_id, obj_type):
    if not request.user.is_authenticated:
        # Determine the appropriate model based on obj_type
        model_class = CustomROM if obj_type == 'rom' else CustomMOD

        # Retrieve the object using the provided obj_id
        try:
            obj = model_class.objects.get(id=obj_id)
            # Perform session tracking here, e.g., updating session data
            if 'visited_objects' not in request.session:
                request.session['visited_objects'] = []
            request.session['visited_objects'].append((obj_type, obj_id))
        except model_class.DoesNotExist:
            pass  # Handle the case where the object doesn't exist

    return HttpResponse("Session tracked for {} ID: {}".format(obj_type.capitalize(), obj_id))

# Create your views here.

def edit_rom(request, rom_id):
    rom = get_object_or_404(CustomROM, id=rom_id)
    
    if request.method == "POST":
        edit_form = UploadROMForm(request.POST, request.FILES, instance=rom)
        if edit_form.is_valid():
            new_image = edit_form.cleaned_data['image']
            edit_form.image = new_image
            edit_form.save()  # Handle image update and upload date retention
            return redirect('custom_roms')  # Successful, redirect back to ROM listing
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
            return redirect('magisk_modules') # Successful, no content

    context = {"edit_form": edit_form, "mod": mod, "mod_id": mod_id}
    return render(request, "edit_mod.html", context)


def search_custom_roms(request):
    query = request.GET.get('q', '')
    if query:
        filtered_roms = CustomROM.objects.filter(
            Q(name__icontains=query) |   # Search by name
            Q(device__icontains=query) |  # Search by device
            Q(credits__icontains=query)   # Search by credits
        )

        roms_data = []
        for rom in filtered_roms:
            likes_count = rom.likes.count()
            rom_data = {
                "id": rom.id,
                "name": rom.name,
                "device": rom.device,
                "details": rom.details,
                "link": rom.link,
                "credits":rom.credits,
                "likes":likes_count,
                "image_url": rom.image.url,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            roms_data.append(rom_data)
    else:
        roms_data = []

    if not roms_data:  # Check if roms_data is empty
        print("No results found")

    print("Saving response data")
    import json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(roms_data, f, ensure_ascii=False, indent=4) 

    return JsonResponse({'results': roms_data})

def search_custom_mods(request):
    query = request.GET.get('q', '')
    if query:
        filtered_mods = CustomMOD.objects.filter(
            Q(name__icontains=query) |   # Search by name
            Q(credits__icontains=query)   # Search by credits
        )

        mods_data = []
        for mod in filtered_mods:
            likes_count = mod.likes.count()
            mod_data = {
                "id": mod.id,
                "name": mod.name,
                "details": mod.details,
                "link": mod.link,
                "credits":mod.credits,
                "likes":likes_count,
                "image_url": mod.image.url,
                "is_staff": request.user.is_staff,
                "is_authenticated": request.user.is_authenticated,
            }
            mods_data.append(mod_data)
    else:
        mods_data = []

    return JsonResponse({'results': mods_data})



def home(request):
    user_profile = UserProfile.objects.all()
    roms = CustomROM.objects.all()
    mods = CustomMOD.objects.all()
    return render(request, "home.html", {'user_profile':user_profile,'roms':roms,'mods':mods})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="app_userprofile/login.html",
        context={"form": form},
    )


def logout_request(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a UserProfile instance for the new user
            UserProfile.objects.create(user=user)

            # Log the user in after registration
            login(request, user)
            return redirect("home")  # Redirect to the home page or a different URL
    else:
        form = SignUpForm()
    return render(request, "app_userprofile/signup.html", {"form": form})



def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user = request.user
    
    if request.method == 'POST':
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES)
        update_username_form = UpdateUsernameForm(request.POST, instance=user)

        if update_username_form.is_valid():
            update_username_form.save()
        
        if profile_picture_form.is_valid():
            new_image = profile_picture_form.cleaned_data['profile_picture']
            user_profile.profile_picture = new_image
            user_profile.save()
            
            return redirect('profile')
    else:
        profile_picture_form = ProfilePictureForm(instance=user_profile)
        update_username_form = UpdateUsernameForm(instance=user)
    
    context = {
        'user_profile': user_profile,
        'profile_picture_form': profile_picture_form,
        'update_username_form': update_username_form,
    }
    
    return render(request, 'profile.html', context)





def custom_roms(request):
    roms = CustomROM.objects.all().order_by('-upload_date')
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
            
            rom_id = request.POST.get('rom_id')
            if rom_id:
                rom = CustomROM.objects.get(pk=rom_id)
                user_liked = rom.likes.filter(id=request.user.id).exists()
                
                if user_liked:
                    rom.likes.remove(request.user)
                else:
                    rom.likes.add(request.user)

                return JsonResponse({'likes': rom.likes.count()})


        else:
            form = UploadROMForm()

        # Format description for each ROM
        for rom in roms:
            rom.formatted_details = mark_safe(
                rom.details.replace("\n", "<br>").replace("-", "&#8226;")
            )
            rom.save()
        return render(request, "custom_roms.html", {"roms": roms,"user_profile": user_profile, "form": form})

    return render(request, "custom_roms.html", {"roms": roms})

def rom_details(request, rom_id):
    rom = get_object_or_404(CustomROM, id=rom_id)
    formatted_details = mark_safe(rom.details.replace("\n", "<br>").replace("-", "&#8226;"))
    return render(request, 'rom_details.html', {'rom': rom, 'formatted_details': formatted_details})

def magisk_modules(request):
    mods = CustomMOD.objects.all().order_by('-upload_date')
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
            
            mod_id = request.POST.get('mod_id')
            if mod_id:
                mod = CustomMOD.objects.get(pk=mod_id)
                user_liked = mod.likes.filter(id=request.user.id).exists()
                
                if user_liked:
                    mod.likes.remove(request.user)
                else:
                    mod.likes.add(request.user)

                return JsonResponse({'likes': mod.likes.count()})


        else:
            form = UploadMODForm()

        # Format description for each mod
        for mod in mods:
            mod.formatted_details = mark_safe(
                mod.details.replace("\n", "<br>").replace("-", "&#8226;")
            )
        
        return render(request, "magisk_modules.html", {"mods": mods,"user_profile": user_profile, "form": form})

    return render(request, "magisk_modules.html", {"mods": mods})


@login_required
@staff_member_required
def manage_user_profiles(request):
    profiles = UserProfile.objects.all()
    return render(
        request, "app_userprofile/manage_user_profiles.html", {"profiles": profiles}
    )


@login_required
@staff_member_required
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
    return render(request,'privacy_policy.html')

""" @login_required
def chat_page(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            direction = ChatMessage.OUTGOING  # The message sender is the logged-in user
            ChatMessage.objects.create(user=request.user, message=message, message_direction=direction)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid form data'})

    form = ChatMessageForm()
    messages = ChatMessage.objects.order_by('-timestamp')[:50]
    user_profile = UserProfile.objects.get(user=request.user)  # Assuming one profile per user
    return render(request, 'chat_page.html', {'messages': messages, 'form': form, 'user_profile': user_profile})

from django.utils.html import escape

from django.http import JsonResponse

from django.utils.html import escape
from app.models import UserProfile  # Make sure to import the UserProfile model

def load_messages(request):
    message_data = []  # Define an empty list outside the branching logic  

    if request.method == 'GET':
        messages = ChatMessage.objects.order_by('-timestamp')[:50]
        for message in messages:
            if message.message_direction == ChatMessage.INCOMING:
                sender_profile = UserProfile.objects.all()
            else:
                sender_profile = None  # Set sender_profile to None for outgoing messages
            message_data.append({
                'content': escape(message.message),
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'direction': message.message_direction,
                'user_profile': sender_profile,
            })
        return JsonResponse({'messages': message_data})
    else:
        return JsonResponse({'messages': []})

 """
from django.shortcuts import render

@csrf_exempt  # Temporarily disable CSRF protection for demonstration purposes
def chatbot(request):
    user_message = ""
    bot_response = ""

    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        # Process user_message and generate a bot response
        bot_response = "XtraBot: I am writing things and he's not giving responses"
        
        return render(request, 'chatbot.html', {'user_message': user_message, 'bot_response': bot_response})

    # For GET requests or other methods, simply render the template
    return render(request, 'chatbot.html', {'user_message': user_message, 'bot_response': bot_response})

import json
import requests
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings

TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    def get(self, request, *args, **kwargs):
        # Handle the GET request here
        # This is where you can respond to Telegram's verification request

        return JsonResponse({'status': 'ok'})

def post(self, request, *args, **kwargs):
    update = json.loads(request.body.decode('utf-8'))
    
    # Print the received update for debugging
    print("Received update:", update)
    
    if 'message' in update and 'chat' in update['message']:
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']
        
        # Process user_message and generate a response
        
        response_message = "You said: " + user_message
        
        # Send the response back to the user
        response_url = TELEGRAM_API_URL + 'sendMessage'
        data = {
            'chat_id': chat_id,
            'text': response_message
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(response_url, json=data, headers=headers)
        
        return JsonResponse({'status': 'ok'})
    else:
        print("Unexpected update structure:", update)
        return JsonResponse({'status': 'error', 'message': 'Invalid update structure'})



# Set up the Telegram webhook URL
TELEGRAM_WEBHOOK_URL = f'https://xtra-roms-l428s43yu-llsiddharthll.vercel.app/telegram/webhook/'  # Replace with your actual URL
webhook_response = requests.post(TELEGRAM_API_URL + 'setWebhook', data={'url': TELEGRAM_WEBHOOK_URL})
if webhook_response.status_code == 200:
    print("Webhook setup successful")
else:
    print("Webhook setup failed")
