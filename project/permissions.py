from rest_framework import permissions


class IsCurrentUserOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author_user_id == request.user
