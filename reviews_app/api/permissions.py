from rest_framework import permissions


class IsReviewerOrReadOnly(permissions.BasePermission):
    """Erlaubt Ändern oder Löschen nur dem Verfasser der Bewertung."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user