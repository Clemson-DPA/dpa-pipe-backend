# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

from rest_framework import serializers
from users.serializers import UserSerializer
from .models import PTask, PTaskVersion, PTaskAssignment

# ----------------------------------------------------------------------------
# Serializer classes:
# ----------------------------------------------------------------------------
class PTaskAssignmentListingField(serializers.RelatedField):
    
    def to_native(self, value):
        return value.user.username

# ----------------------------------------------------------------------------
class PTaskStatusField(serializers.ChoiceField):
   
    def to_native(self, value):
        value = super(PTaskStatusField, self).to_native(value) 
        for (status, status_str) in PTask.STATUS_CHOICES:
            if status == value:
                return status_str
        return value
    
    def from_native(self, value):
        value = super(PTaskStatusField, self).from_native(value) 
        for (status, status_str) in PTask.STATUS_CHOICES:
            if status_str == value:
                return status
        return value

# ----------------------------------------------------------------------------
class PTaskSerializer(serializers.ModelSerializer):

    assignments = PTaskAssignmentListingField(many=True, required=False)
    children = serializers.RelatedField(many=True, required=False)
    creator = serializers.SlugRelatedField(slug_field="username")
    start_date = serializers.DateField()
    due_date = serializers.DateField(required=False)
    parent = serializers.SlugRelatedField(slug_field="spec", required=False)
    ptask_type = serializers.SlugRelatedField(slug_field="name")
    versions = serializers.RelatedField(many=True, required=False)
    status = PTaskStatusField(choices=PTask.STATUS_CHOICES)

    class Meta:
        model = PTask

        exclude = (

            # mptt fields
            "lft",
            "rght",
            "tree_id",
            "level",
        )

# ----------------------------------------------------------------------------
class PTaskVersionSerializer(serializers.ModelSerializer):

    children = serializers.RelatedField(many=True)
    creator = serializers.SlugRelatedField(slug_field="username")
    description = serializers.CharField(required=False)
    location = serializers.SlugRelatedField(slug_field="code")
    parent = serializers.SlugRelatedField(slug_field="spec", required=False)
    ptask = serializers.SlugRelatedField(slug_field="spec")
    
    class Meta:
        model = PTaskVersion

        exclude = (

            # mptt fields
            "lft",
            "rght",
            "tree_id",
            "level",
        )

# ----------------------------------------------------------------------------
class PTaskAssignmentSerializer(serializers.ModelSerializer):

    ptask = serializers.SlugRelatedField(slug_field="spec")
    user = serializers.SlugRelatedField(slug_field="username")
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    class Meta:
        model = PTaskAssignment

