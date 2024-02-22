from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 2)


class IsAdmin(BasePermission):
    """
     Allows access only to authenticated admin.
     """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 1)


