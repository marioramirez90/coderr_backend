from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Erlaubt lesenden Zugriff für alle authentifizierten Nutzer,
    aber Schreibzugriff (PATCH/PUT) nur dem Profil-Eigentümer.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user