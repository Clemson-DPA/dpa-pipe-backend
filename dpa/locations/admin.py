# -----------------------------------------------------------------------------
# Module: dpa.locations.models
# Author: Josh Tomlinson (jtomlin)
# -----------------------------------------------------------------------------
"""Define the admin interface for the locations app."""

# -----------------------------------------------------------------------------
# Imports:
# -----------------------------------------------------------------------------
 
from django.contrib import admin
from locations.models import Location

# -----------------------------------------------------------------------------
# Model Registration:
# -----------------------------------------------------------------------------
class LocationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'host', 'filesystem_root', 'description', 'active')

admin.site.register(Location, LocationAdmin)

