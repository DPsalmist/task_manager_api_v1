from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (GET, HEAD, OPTIONS) are allowed if owner
        return obj.owner == request.user


class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to allow only project owners to access related tasks.
    """

    def has_object_permission(self, request, view, obj):
        # obj is Task instance
        return obj.project.owner == request.user
