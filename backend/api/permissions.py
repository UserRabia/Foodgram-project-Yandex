from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AdminOrAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user):
            return True
        raise PermissionDenied(
            "У Вас недостаточно прав для выполения этого действия"
        )
