from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        exclude = (
            "date_joined",
            "groups",
            "last_login",
            "password",
            "user_permissions",
        )

