"""
Custom permissions for the offers REST API endpoints.
"""

from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Permission check to allow access only to users with a business profile.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "business"
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission check to allow object modification only to the owner of the offer.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user