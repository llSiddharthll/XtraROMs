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
import random

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
        if user.is_authorized:
            user.is_authorized = False
            user.save()
            messages.success(request, f"{user.user.username} is unauthorized")
            return JsonResponse({"success": "success"})
        else:
            user.is_authorized =True
            user.save()
            messages.success(request, f"{user.user.username} is authorized")
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
        upload_blog = uploadBlogForm()
        user_form = UserProfileForm(instance=user_profile)  # Use instance=user_profile for the user form
        liked_roms = ROMLike.objects.filter(user=request.user)
        liked_mods = MODLike.objects.filter(user=request.user)
        blogs = Blog.objects.filter(written_by=request.user)

        context = {
            "user_profile": user_profile,
            "liked_roms": liked_roms,
            "liked_mods": liked_mods,
            "rom_form": rom_form,
            "mod_form": mod_form,
            "upload_blog": upload_blog,
            "user_form": user_form,
            "blogs": blogs
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
    
class RomsView(generic.ListView):
    template_name = 'roms.html'
    model = CustomROM
    paginate_by = 12
    context_object_name = 'roms'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-upload_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked_rom_ids = set(ROMLike.objects.filter(rom__in=context['roms'], user=self.request.user).values_list('rom_id', flat=True))
            context['liked_rom_ids'] = liked_rom_ids
            
        likes_count_dict = {}
        for rom in context['roms']:
            likes_count = ROMLike.objects.filter(rom=rom).count()
            likes_count_dict[rom.id] = likes_count
        context['likes'] = likes_count_dict

        return context
    
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
        suggested_roms = CustomROM.objects.filter(device__in=rom.device.all())

        formatted_details = mark_safe(
            rom.details.replace("\n", "<br>").replace("-", "&#8226;")
        )
        comments = rom.comments.order_by('-created_at')
        form = CommentForm()
        return render(
            request,
            self.template_name,
            {"rom": rom, "formatted_details": formatted_details, "comments": comments, "form": form, "suggested_roms": suggested_roms},
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
    
class ModsView(generic.ListView):
    template_name = 'mods.html'
    model = CustomMOD
    context_object_name = 'mods'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-upload_date')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a flag indicating whether the user has liked each mod
        if self.request.user.is_authenticated:
            liked_mod_ids = set(MODLike.objects.filter(mod__in=context['mods'], user=self.request.user).values_list('mod_id', flat=True))
            context['liked_mod_ids'] = liked_mod_ids
            
        # Dictionary to store likes count for each mod
        likes_count_dict = {}
        
        # Calculate likes count for each mod
        for mod in context['mods']:
            likes_count = MODLike.objects.filter(mod=mod).count()
            likes_count_dict[mod.id] = likes_count
        
        context['likes'] = likes_count_dict

        return context
    
    def post(self, request, *args, **kwargs):
        mod_id = request.POST.get("modID")
        if mod_id is not None:
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
        suggested_mods = CustomMOD.objects.all()
        suggested_mods = list(suggested_mods)
        random.shuffle(suggested_mods)
        random_mods = random.sample(suggested_mods, 6)
        formatted_details = mark_safe(
            mod.details.replace("\n", "<br>").replace("-", "&#8226;")
        )
        comments = mod.comments.order_by('-created_at')
        form = CommentForm()
        return render(
            request,
            self.template_name,
            {"mod": mod, "formatted_details": formatted_details, "comments": comments, "form": form, "random_mods": random_mods},
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
        upload_blog = uploadBlogForm()
        context = {'blogs': blog, 'upload_blog': upload_blog}
        return render(request, self.template_name, context)
    
    
class DetailsView(generic.View):
    template_name = "details.html"

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        return render(request, self.template_name, {'blog': blog})
    
class PolicyView(generic.TemplateView):
    template_name = "privacy_policy.html"
    
