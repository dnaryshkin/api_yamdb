from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
