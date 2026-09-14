from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "customer"
        )


class IsOrderBusinessUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.type == "business"
        )

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
