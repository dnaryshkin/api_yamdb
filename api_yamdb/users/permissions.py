from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Права модератора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator()


class IsAdmin(permissions.BasePermission):
    """Права администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()
