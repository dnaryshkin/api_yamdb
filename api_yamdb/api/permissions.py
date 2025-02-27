from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Класс предоставляющий доступ админу или
    get запрос от пользователя без токена.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthUserOrAuthorOrModerOrAdminOrReadOnly(BasePermission):
    """
    Класс предоставляющий доступ при get запросе всем пользователям,
    при post запросе только аутентифицированным пользователям,
    при patch и delete запросе автору, модератору, админу.
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
