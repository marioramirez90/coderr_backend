from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """lesenden Zugriff....aber nur Besitzer dürfen verändern."""

    def has_object_permission(self, request, view, obj):
        """Prüft Benutzer"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user