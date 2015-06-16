# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

from rest_framework import serializers
from users.serializers import UserSerializer
from .models import (
    ProductCategory,
    Product,
    ProductVersion,
    ProductRepresentation,
    ProductGrouping,
    ProductRepresentationStatus,
    ProductSubscription,
)

# ----------------------------------------------------------------------------
class ProductRepresentationStatusField(serializers.ChoiceField):
   
    def to_native(self, value):
        value = super(ProductRepresentationStatusField, self).from_native(value) 
        for (status, status_str) in ProductRepresentationStatus.STATUS_CHOICES:
            if status == value:
                return status_str
        return value
    
    def from_native(self, value):
        value = super(ProductRepresentationStatusField, self).from_native(value) 
        for (status, status_str) in ProductRepresentationStatus.STATUS_CHOICES:
            if status_str == value:
                return status
        return value

# ----------------------------------------------------------------------------
class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory

# ----------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):

    ptask = serializers.SlugRelatedField(slug_field="spec")
    category = serializers.SlugRelatedField(slug_field="name")
    creator = serializers.SlugRelatedField(slug_field="username")
    versions = serializers.RelatedField(many=True, required=False)

    class Meta:
        model = Product

# ----------------------------------------------------------------------------
class ProductVersionSerializer(serializers.ModelSerializer):

    ptask_version = serializers.SlugRelatedField(slug_field="spec")
    product = serializers.SlugRelatedField(slug_field="spec")
    creator = serializers.SlugRelatedField(slug_field="username")

    class Meta:
        model = ProductVersion

# ----------------------------------------------------------------------------
class ProductRepresentationSerializer(serializers.ModelSerializer):

    product_version = serializers.SlugRelatedField(slug_field="spec")
    creation_location = serializers.SlugRelatedField(slug_field="code")
    creator = serializers.SlugRelatedField(slug_field="username")

    class Meta:
        model = ProductRepresentation

# ----------------------------------------------------------------------------
class ProductRepresentationStatusSerializer(serializers.ModelSerializer):

    product_representation = serializers.SlugRelatedField(slug_field="spec")
    location = serializers.SlugRelatedField(slug_field="code")
    status = ProductRepresentationStatusField(
        choices=ProductRepresentationStatus.STATUS_CHOICES)

    class Meta:
        model = ProductRepresentationStatus

# ----------------------------------------------------------------------------
class ProductGroupingSerializer(serializers.ModelSerializer):
    
    parent_product_version = serializers.SlugRelatedField(slug_field="spec")
    child_product_version = serializers.SlugRelatedField(slug_field="spec")

    class Meta:
        model = ProductGrouping

# ----------------------------------------------------------------------------
class ProductSubscriptionSerializer(serializers.ModelSerializer):
    
    product_version = serializers.SlugRelatedField(slug_field="spec")
    ptask_version = serializers.SlugRelatedField(slug_field="spec")

    class Meta:
        model = ProductSubscription

