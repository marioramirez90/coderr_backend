from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """GET /api/profile/{pk}/ und PATCH /api/profile/{pk}/."""

    def has_object_permission(self, request, view, obj):
        """lese anfrage get ,head, options"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
        """patch put anfrage """
