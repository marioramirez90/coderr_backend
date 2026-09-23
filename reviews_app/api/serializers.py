"""
Serializers for the reviews REST API endpoints.

Handles serialization and validation for reviews, including self-review prevention.
"""

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source="reviewer.id")

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        business_user = attrs.get("business_user")

        # Prevent self-review (returns 403 Forbidden)
        if request and request.user == business_user:
            raise PermissionDenied("You cannot review yourself.")

        return attrs

    def create(self, validated_data):
        validated_data["reviewer"] = self.context["request"].user
        return super().create(validated_data)