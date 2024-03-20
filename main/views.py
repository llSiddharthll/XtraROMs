from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import *
from .forms import *
from django.db.models import Count
from allauth.account.views import SignupView, LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.contrib import messages
import json

class HomeView(generic.View):
    template_name = "home.html"
    
    def get(self, request, *args, **kwargs):
        context = {}
        
        roms = CustomROM.objects.all().order_by('-upload_date')[:3]
        context['roms'] = roms
        rom = context.get('roms')
        if rom:
            likes_count_dict = {}
            for rom in roms:
                likes_count = ROMLike.objects.filter(rom=rom).count()
                likes_count_dict[rom.id] = likes_count

            context['likes'] = likes_count_dict
            comment_count_dict = {}
            for rom in roms:
                comment_count = RomComment.objects.filter(rom=rom).count()
                comment_count_dict[rom.id] = comment_count
            
            context['comment'] = comment_count_dict
            context['total_users'] = User.objects.count()
            context['total_items'] = CustomMOD.objects.count() + CustomROM.objects.count()
        
        return render(request, self.template_name, context)

class ManageUserView(generic.ListView):
    model = UserProfile
    context_object_name = 'users'
    template_name = 'manage_users.html'
    
    def post(self, request):
        id = request.POST.get("id")
        user = UserProfile.objects.get(id=id)
        authorized = request.POST.get("request")
        if authorized == "authorize":
            if user.is_authorized == True:
                return JsonResponse({"error": "already_authorized"})
            else:
                user.is_authorized = True
                user.save()
                return JsonResponse({"success": "success"})
        else:
            if user.is_authorized == False:
                return JsonResponse({"error": "already_unauthorized"})
            else:
                user.is_authorized = False
                user.save()
                return JsonResponse({"success": "success"})
        
class SignupView(SignupView):
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

    
class LoginView(LoginView):
    template_name = 'account/login.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
class DashboardView(generic.View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        rom_form = UploadROMForm()
        mod_form = UploadMODForm()
        user_form = UserProfileForm(instance=user_profile)  # Use instance=user_profile for the user form
        liked_roms = ROMLike.objects.filter(user=request.user)
        liked_mods = MODLike.objects.filter(user=request.user)
        
        context = {
            "user_profile": user_profile,
            "liked_roms": liked_roms,
            "liked_mods": liked_mods,
            "rom_form": rom_form,
            "mod_form": mod_form,
            "user_form": user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_profile = request.user.userprofile
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # Instantiate form for POST requests
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('dashboard')  # Redirect to the dashboard page after profile update
        
        # If form is not valid, render the dashboard page with the form
        return render(request, self.template_name, {"user_form": form})
    
class RomsView(generic.View):
    template_name = 'roms.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        roms = CustomROM.objects.all().order_by('-upload_date')
        context['roms'] = roms
        
        # Add a flag indicating whether the user has liked each ROM
        roms = context.get('roms')
        if roms:
            if request.user.is_authenticated:
                liked_rom_ids = set(ROMLike.objects.filter(rom__in=roms, user=request.user).values_list('rom_id', flat=True))
                context['liked_rom_ids'] = liked_rom_ids
            
            # Dictionary to store likes count for each ROM
            likes_count_dict = {}

            # Calculate likes count for each ROM
            for rom in roms:
                likes_count = ROMLike.objects.filter(rom=rom).count()
                likes_count_dict[rom.id] = likes_count

            context['likes'] = likes_count_dict

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        rom_id = request.POST.get("romID")
        if rom_id is not None:
            # Rest of your code...
            rom = get_object_or_404(CustomROM, id=rom_id)
            like, created = ROMLike.objects.get_or_create(user=request.user, rom=rom)

            if not created:
                # If the user already liked it, unlike it
                like.delete()
                return JsonResponse({"status": "unliked"})
            else:
                return JsonResponse({"status": "liked"})
        else:
            return JsonResponse({"status": "error", "message": "'romID' not found in POST data"})

class ROMDetailsView(generic.View):
    template_name = 'rom_details.html'
    context_object_name = 'rom'

    def get(self, request, slug):
        rom = get_object_or_404(CustomROM, slug=slug)
        formatted_details = mark_safe(
            rom.details.replace("\n", "<br>").replace("-", "&#8226;")
        )
        comments = rom.comments.order_by('-created_at')
        form = CommentForm()
        return render(
            request,
            self.template_name,
            {"rom": rom, "formatted_details": formatted_details, "comments": comments, "form": form},
        )

    def post(self, request, slug):
        rom = get_object_or_404(CustomROM, slug=slug)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            rom.comments.add(comment)
            
            return redirect("rom_details", rom.slug)

        return JsonResponse({"error": "Invalid POST request"})
    
class ModsView(generic.View):
    template_name = 'mods.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        mods = CustomMOD.objects.all().order_by('-upload_date')
        context['mods'] = mods
        
        # Add a flag indicating whether the user has liked each mod
        mods = context.get('mods')
        if mods:
            if request.user.is_authenticated:
                liked_mod_ids = set(MODLike.objects.filter(mod__in=mods, user=request.user).values_list('mod_id', flat=True))
                context['liked_mod_ids'] = liked_mod_ids
            
            # Dictionary to store likes count for each mod
            likes_count_dict = {}

            # Calculate likes count for each mod
            for mod in mods:
                likes_count = MODLike.objects.filter(mod=mod).count()
                likes_count_dict[mod.id] = likes_count

            context['likes'] = likes_count_dict

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        mod_id = request.POST.get("modID")
        if mod_id is not None:
            # Rest of your code...
            mod = get_object_or_404(CustomMOD, id=mod_id)
            like, created = MODLike.objects.get_or_create(user=request.user, mod=mod)

            if not created:
                # If the user already liked it, unlike it
                like.delete()
                return JsonResponse({"status": "unliked"})
            else:
                return JsonResponse({"status": "liked"})
        else:
            return JsonResponse({"status": "error", "message": "'modID' not found in POST data"})
    
class MODDetailsView(generic.View):
    template_name = 'mod_details.html'
    context_object_name = 'mod'

    def get(self, request, slug):
        mod = get_object_or_404(CustomMOD, slug=slug)
        formatted_details = mark_safe(
            mod.details.replace("\n", "<br>").replace("-", "&#8226;")
        )
        comments = mod.comments.order_by('-created_at')
        form = CommentForm()
        return render(
            request,
            self.template_name,
            {"mod": mod, "formatted_details": formatted_details, "comments": comments, "form": form},
        )

    def post(self, request, slug):
        mod = get_object_or_404(CustomMOD, slug=slug)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            mod.comments.add(comment)
            
            return redirect("mod_details", mod.slug)

        return JsonResponse({"error": "Invalid POST request"})
    
class XtraKnowledgeView(generic.ListView):
    template_name = "xtraknowledge.html"
    
    def get(self, request):
        blog = Blog.objects.all()
        context = {'blogs': blog}
        return render(request, self.template_name, context)
    
class PolicyView(generic.TemplateView):
    template_name = "privacy_policy.html"
    
