from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    """Права модератора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(BasePermission):
    """Права администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Класс предоставляющий доступ админу или
    GET запрос доступен всем пользователям.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrStaff(BasePermission):
    """
    GET-запросы доступны всем пользователям;
    POST-запросы доступны только аутентифицированным пользователям;
    PATCH и DELETE-запросы доступны автору, модератору или администратору.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
