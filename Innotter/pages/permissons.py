from rest_framework import permissions

from users.models import User


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == User.Roles.ADMIN


class IsModeratorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role == User.Roles.MODERATOR


class IsWelcome(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if (
            not obj.is_private
            or user.role != User.Roles.USER
            or user in obj.followers.all()
            or user == obj.owner
        ):
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        return user == obj.owner


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        return user == obj.page.owner


class IsAlreadyWelcomed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        IsWelcome.has_object_permission(request, view, obj.page)


class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_blocked


class IsNotBlacklisted(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user not in obj.blacklisted_users.all()


class DictionaryPermissionsMixin:
    def get_permissions(self):
        return [permission() for permission in self.permission_classes.get(self.action)]

