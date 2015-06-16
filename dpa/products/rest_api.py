
# ----------------------------------------------------------------------------
# Imports:
# ----------------------------------------------------------------------------

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

import django_filters

from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from .models import (
    ProductCategory,
    Product,
    ProductVersion,
    ProductRepresentation,
    ProductGrouping,
    ProductRepresentationStatus,
    ProductSubscription,
)

from .serializers import (
    ProductCategorySerializer,
    ProductSerializer,
    ProductVersionSerializer,
    ProductRepresentationSerializer,
    ProductGroupingSerializer,
    ProductRepresentationStatusSerializer,
    ProductSubscriptionSerializer,
)

# ----------------------------------------------------------------------------
# Filter classes:
# ----------------------------------------------------------------------------
class ListFilter(django_filters.Filter):

    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, [value.split(","), 'in'])

# ----------------------------------------------------------------------------
class ProductFilterSet(django_filters.FilterSet):

    category = django_filters.CharFilter(name="category__name")
    creator = django_filters.CharFilter(name="creator__username")
    ids = ListFilter(name="id")
    ptask = django_filters.CharFilter(name="ptask__spec")
    specs = ListFilter(name="spec")
    
    class Meta:
        model = Product
        fields = [
            "category",
            "creator",
            "id",
            "ids",
            "name",
            "ptask",
            "spec",
            "specs",
        ]

# ----------------------------------------------------------------------------
class ProductVersionFilterSet(django_filters.FilterSet):

    creator = django_filters.CharFilter(name="creator__username")
    ids = ListFilter(name="id")
    product = django_filters.CharFilter(name="product__spec")
    ptask = django_filters.CharFilter(name="ptask_version__ptask__spec")
    ptask_version = django_filters.CharFilter(name="ptask_version__spec")
    specs = ListFilter(name="spec")
    
    class Meta:
        model = ProductVersion 
        fields = [
            "creator",
            "deprecated",
            "id",
            "ids",
            "number",
            "product",
            "ptask_version",
            "published",
            "spec",
            "specs",
        ]

# ----------------------------------------------------------------------------
class ProductRepresentationFilterSet(django_filters.FilterSet):

    creation_location = django_filters.CharFilter(
        name="creation_location__code")
    creator = django_filters.CharFilter(name="creator__username")
    ids = ListFilter(name="id")
    product_version = django_filters.CharFilter(name="product_version__spec")
    specs = ListFilter(name="spec")

    class Meta:
        model = ProductRepresentation
        fields = [
            "creation_location",
            "creator",
            "frame_range",
            "id",
            "ids",
            "product_version",
            "resolution",
            "representation_type",
            "spec",
            "specs",
        ]

# ----------------------------------------------------------------------------
class ProductRepresentationStatusFilterSet(django_filters.FilterSet):

    ids = ListFilter(name="id")
    location = django_filters.CharFilter(name="location__code")
    product_representation = django_filters.CharFilter(
        name="product_representation__spec")
    specs = ListFilter(name="spec")

    class Meta:
        model = ProductRepresentationStatus
        fields = [
            "id",
            "ids",
            "location",
            "product_representation",
            "spec",
            "specs",
            "status",
        ]

# ----------------------------------------------------------------------------
class ProductGroupingFilterSet(django_filters.FilterSet):

    child = django_filters.CharFilter(name="child_product_version__spec")
    ids = ListFilter(name="id")
    parent = django_filters.CharFilter(name="parent_product_version__spec")
    ptask = django_filters.CharFilter(
        name="parent_product_version__ptask_version__ptask__spec"
    )
    ptask_version = django_filters.CharFilter(
        name="parent_product_version__ptask_version__spec"
    )
    specs = ListFilter(name="spec")
    
    class Meta:
        model = ProductGrouping
        fields = [
            "child",
            "id",
            "ids",
            "parent",
            "ptask",
            "ptask_version",
            "spec",
            "specs",
        ]

# ----------------------------------------------------------------------------
class ProductSubscriptionFilterSet(django_filters.FilterSet):
        
    ids = ListFilter(name="id")
    product_version = django_filters.CharFilter(name="product_version__spec")
    ptask_version = django_filters.CharFilter(name="ptask_version__spec")
    product = django_filters.CharFilter(name="product_version__product__spec")
    ptask = django_filters.CharFilter(name="ptask_version__ptask__spec")

    class Meta:
        model = ProductSubscription
        fields = [
            "id",
            "ids",
            "product_version",
            "ptask_version",
            "product",
            "ptask",
            "locked",
        ]

# ----------------------------------------------------------------------------
# ViewSets:
# ----------------------------------------------------------------------------
class ProductCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

# ----------------------------------------------------------------------------
class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filter_class = ProductFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ("spec",)

# ----------------------------------------------------------------------------
class ProductVersionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filter_class = ProductVersionFilterSet
    filter_fields = ('id','number')
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionSerializer

# ----------------------------------------------------------------------------
class ProductRepresentationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filter_class = ProductRepresentationFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = ProductRepresentation.objects.all()
    serializer_class = ProductRepresentationSerializer

# ----------------------------------------------------------------------------
class ProductRepresentationStatusViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filter_class = ProductRepresentationStatusFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = ProductRepresentationStatus.objects.all()
    serializer_class = ProductRepresentationStatusSerializer

# ----------------------------------------------------------------------------
class ProductGroupingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filter_class = ProductGroupingFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = ProductGrouping.objects.all()
    serializer_class = ProductGroupingSerializer

# ----------------------------------------------------------------------------
class ProductSubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):


    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filter_class = ProductSubscriptionFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = ProductSubscription.objects.all()
    serializer_class = ProductSubscriptionSerializer
    search_fields = ("spec",)

