from urllib import request
from rest_framework import permissions
from users.verify import JWTAuthentication
from users.models import User


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = JWTAuthentication().authenticate(request)[0]
        return user.role == User.Roles.ADMIN
    

class IsModeratorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = JWTAuthentication().authenticate(request)[0]
        return user.role == User.Roles.MODERATOR
    
class IsWelcome(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = JWTAuthentication().authenticate(request)[0]
        if not obj.is_private:
            return True
        elif user.role != User.Roles.USER or user in obj.followers.all() or user == obj.owner:
            return True
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = JWTAuthentication().authenticate(request)[0]
        if request.method in permissions.SAFE_METHODS:
            return True
        return user == obj.owner
    
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = JWTAuthentication().authenticate(request)[0]
        if request.method in permissions.SAFE_METHODS:
            return True
        return user == obj.page.owner
    
class IsAlreadyWelcomed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        IsWelcome.has_object_permission(request, view, obj.page)
        
        