
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
    PTask,
    PTaskAssignment,
    PTaskVersion,
)

from .serializers import (
    PTaskAssignmentSerializer,
    PTaskSerializer,
    PTaskVersionSerializer,
)

# ----------------------------------------------------------------------------
# Filter classes:
# ----------------------------------------------------------------------------
class ListFilter(django_filters.Filter):

    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, [value.split(","), 'in'])

# ----------------------------------------------------------------------------
class PTaskFilterSet(django_filters.FilterSet):

    # rename related fields for ease of use
    creator = django_filters.CharFilter(name="creator__username")
    ids = ListFilter(name="id")
    parent = django_filters.CharFilter(name="parent__spec")
    ptask_type = django_filters.CharFilter(name="ptask_type__name")
    specs = ListFilter(name="spec")

    class Meta:
        model = PTask
        fields = [
            "active", 
            "creator",
            "id",
            "ids",
            "name", 
            "parent",
            "ptask_type", 
            "spec",
            "specs",
            "status", 
        ]

# ----------------------------------------------------------------------------
class PTaskAssignmentFilterSet(django_filters.FilterSet):

    # rename related fields for ease of use
    ptask = django_filters.CharFilter(name="ptask__spec")
    ptasks = ListFilter(name="ptask__spec")
    user = django_filters.CharFilter(name="user__username")
    users= ListFilter(name="user__username")

    class Meta:
        model = PTaskAssignment
        fields = [
            "ptask",
            "ptasks",
            "user",
            "users",
        ]

# ----------------------------------------------------------------------------
class PTaskVersionFilterSet(django_filters.FilterSet):

    # rename related fields for ease of use
    creator = django_filters.CharFilter(name="creator__username")
    ids = ListFilter(name="id")
    location = django_filters.CharFilter(name="location__code")
    ptask = django_filters.CharFilter(name="ptask__spec")
    parent = django_filters.CharFilter(name="parent__spec")
    specs = ListFilter(name="spec")

    class Meta:
        model = PTaskVersion
        fields = [
            "creator",
            "id", 
            "ids", 
            "location",
            "number",
            "parent",
            "ptask",
            "spec",
            "specs",
        ]

# ----------------------------------------------------------------------------
# ViewSet classes:
# ----------------------------------------------------------------------------
class PTaskViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """API endpoint that allows ptasks to be viewed and edited."""

    # ------------------------------------------------------------------------
    # Class attributes:
    # ------------------------------------------------------------------------

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filter_class = PTaskFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = PTask.objects.all()
    serializer_class = PTaskSerializer
    search_fields = ("spec",)

# ----------------------------------------------------------------------------
class PTaskVersionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """API endpoint that allows ptask versions to be viewed and edited."""

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filter_class = PTaskVersionFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = PTaskVersion.objects.all()
    serializer_class = PTaskVersionSerializer

# ----------------------------------------------------------------------------
class PTaskAssignmentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):

    # ------------------------------------------------------------------------
    # Class attributes:
    # ------------------------------------------------------------------------
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )

    filter_class = PTaskAssignmentFilterSet
    filter_fields = ('id',)
    lookup_field = "spec"
    ordering = ("spec",)
    ordering_fields = ("spec",)
    queryset = PTaskAssignment.objects.all()
    serializer_class = PTaskAssignmentSerializer

