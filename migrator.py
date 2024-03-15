import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XtraROMs.settings')

# Configure Django
django.setup()

from main.models import CustomROM, CustomMOD
from django.utils.text import slugify

roms_without_slugs = CustomROM.objects.filter(slug="undefined")
for rom in roms_without_slugs:
    # Generate slug from the ROM name
    rom_slug = slugify(rom.name)
    # Update the slug field
    rom.slug = rom_slug
    rom.save()
mods_without_slugs = CustomMOD.objects.filter(slug="undefined")
for mod in mods_without_slugs:
    mod_slug = slugify(mod.name)
    mod.slug = mod_slug
    mod.save()
    