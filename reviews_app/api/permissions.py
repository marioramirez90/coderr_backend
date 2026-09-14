from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Nur authentifizierte Benutzer mit Kundenprofil dürfen bewerten."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsReviewerOrReadOnly(permissions.BasePermission):
    """Erlaubt Ändern oder Löschen nur dem Verfasser der Bewertung."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user