from rest_framework import permissions

from project.models import Contributor


class IsProjectAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author_user_id == request.user
