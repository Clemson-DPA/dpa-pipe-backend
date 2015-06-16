from rest_framework import viewsets
from rest_framework.filters import (
    DjangoFilterBackend,
    OrderingFilter,
    SearchFilter,
)

from .models import Location
from .serializers import LocationSerializer

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows locations to be viewed."""

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filter_fields = (
        "code",
        "name",
        "timezone",
        "active",
    )

    search_fields = (
        "code",
        "name",
        "description",
        "timezone"
    )

    ordering_fields = (
        "code",
        "name",
        "description",
        "timezone"
    )

    ordering = ("name",)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

