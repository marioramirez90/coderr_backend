"""
Custom permissions for the reviews REST API endpoints.
"""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """
    Only authenticated users with a customer profile are allowed to create reviews.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsReviewerOrReadOnly(permissions.BasePermission):
    """
    Allows modification or deletion only to the author of the review.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user