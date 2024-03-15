import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XtraROMs.settings')

# Configure Django
django.setup()

from main.models import CustomROM, CustomMOD
from django.utils.text import slugify
import uuid

roms_without_slugs = CustomROM.objects.all()
for rom in roms_without_slugs:
    # Generate slug from the ROM name
    """ rom_slug = slugify(rom.name)
    unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
    rom_slug = f"{rom_slug}-{unique_id}"
    rom.slug = rom_slug """
    if rom.slug:
        rom.slug = None
    rom.save()
mods_without_slugs = CustomMOD.objects.all()
for mod in mods_without_slugs:
    """ mod_slug = slugify(mod.name)
    unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
    mod_slug = f"{mod_slug}-{unique_id}"
    mod.slug = mod_slug """
    if mod.slug:
        mod.slug = None
    mod.save()
    