"""
Serializers for the authentication REST API endpoints.

Handles user registration, login authentication, and user profile management.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration at /api/registration/."""

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=UserProfile.TYPE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """Validate password matching."""
        if attrs.get("password") != attrs.get("repeated_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """Create a new User and associated UserProfile."""
        account_type = validated_data.pop("type")
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, type=account_type)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login at /api/login/."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate user credentials and authenticate."""
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password")
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile management at /api/profile/."""

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True, default="")
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True, default="")
    email = serializers.EmailField(source="user.email", required=False, allow_blank=True, default="")

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "type", "created_at"]

    def to_representation(self, instance):
        """Ensure None values in text fields are converted to empty strings."""
        data = super().to_representation(instance)
        text_fields = ["first_name", "last_name", "location", "tel", "description", "working_hours"]
        for field in text_fields:
            if data.get(field) is None:
                data[field] = ""
        return data

    def update(self, instance, validated_data):
        """Update UserProfile instance and associated User fields."""
        user_data = validated_data.pop("user", {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        return super().update(instance, validated_data)