from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters

from .serializers import UserSerializer

# API
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows users to be viewed."""

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filter_fields = (
        "id", 
        "username", 
        "first_name", 
        "last_name", 
        "email",
        "is_staff", 
        "is_active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    ordering_fields = (
        "first_name",
        "last_name",
        "email",
    )

    lookup_field = "username"
    ordering = ("last_name", "first_name", "email")
    queryset = User.objects.all()
    serializer_class = UserSerializer

