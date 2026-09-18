"""
Custom permissions for the orders REST API endpoints.
"""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """
    Permission check to allow order creation only to users with a customer profile.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsOrderBusinessUser(permissions.BasePermission):
    """
    Permission check to allow order updates only to the assigned business user.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "business"
        )

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user

