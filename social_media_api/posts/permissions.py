# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only owners may edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Read perms allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise only owner
        return obj.author == request.user
