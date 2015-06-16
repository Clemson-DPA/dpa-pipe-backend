# -----------------------------------------------------------------------------
# Module: dpa.ptasks.models
# Author: Josh Tomlinson (jtomlin)
# -----------------------------------------------------------------------------
"""Define the admin interface for the ptasks app."""

# -----------------------------------------------------------------------------
# Imports:
# -----------------------------------------------------------------------------
 
from django.contrib import admin
from ptasks.models import PTask, PTaskType, PTaskAssignment, PTaskVersion

# -----------------------------------------------------------------------------
# Model Registration:
# -----------------------------------------------------------------------------
class PTaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'level_hint')

# -----------------------------------------------------------------------------
class PTaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('spec', 'ptask_type', 'status', 'start_date', 'due_date')

# -----------------------------------------------------------------------------
class PTaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ptask', 'start_date', 'end_date', 'active')

# -----------------------------------------------------------------------------
class PTaskVersionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('spec',)

# -----------------------------------------------------------------------------
# Register admin views
# -----------------------------------------------------------------------------
admin.site.register(PTaskType, PTaskTypeAdmin)
admin.site.register(PTask, PTaskAdmin)
admin.site.register(PTaskAssignment, PTaskAssignmentAdmin)
admin.site.register(PTaskVersion, PTaskVersionAdmin)

