from rest_framework import permissions

class CanEditPhotoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.groups.filter(name='noivos').exists() or user.groups.filter(name='amigos').exists()):
            return True
        return False
