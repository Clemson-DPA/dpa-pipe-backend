
# -----------------------------------------------------------------------------
# Imports:
# -----------------------------------------------------------------------------
 
from django.contrib import admin
from products.models import (
    ProductCategory,
    Product,
    ProductVersion,
    ProductRepresentation,
    ProductRepresentationStatus,
    ProductGrouping,
    ProductSubscription,
)

# ----------------------------------------------------------------------------
# Model registration:
# ----------------------------------------------------------------------------
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'description'
    )

# ----------------------------------------------------------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'spec',
        'description',
    )

# ----------------------------------------------------------------------------
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = (
        'spec',
        'published',
        'deprecated',
        'release_note',
    )

# ----------------------------------------------------------------------------
class ProductRepresentationAdmin(admin.ModelAdmin):
    list_display = (
        'spec',
        'creator',
    )

# ----------------------------------------------------------------------------
class ProductRepresentationStatusAdmin(admin.ModelAdmin):
    list_display = (
        'product_representation',
        'location',
        'status'
    )

# ----------------------------------------------------------------------------
class ProductGroupingAdmin(admin.ModelAdmin):
    list_display = (
        'parent_product_version',
        'child_product_version',
    )

# ----------------------------------------------------------------------------
class ProductSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'product_version',
        'ptask_version',
        'locked',
    )

# -----------------------------------------------------------------------------
# Register admin views:
# -----------------------------------------------------------------------------
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVersion, ProductVersionAdmin)
admin.site.register(ProductRepresentation, ProductRepresentationAdmin)
admin.site.register(ProductRepresentationStatus, 
    ProductRepresentationStatusAdmin)
admin.site.register(ProductGrouping, ProductGroupingAdmin)
admin.site.register(ProductSubscription, ProductSubscriptionAdmin)

