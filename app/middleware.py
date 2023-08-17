# middleware.py
from .models import CustomROM, CustomMOD
from .views import track_session

class SessionTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            # Perform session tracking for anonymous users only on specific pages
            if request.path in ['/roms/', '/mods/']:  # Adjust URLs as needed
                roms = CustomROM.objects.all()  # You can also filter the records here
                mods = CustomMOD.objects.all()  # You can also filter the records here

                for rom in roms:
                    track_session(request, rom.id)

                for mod in mods:
                    track_session(request, mod.id)

        return response
