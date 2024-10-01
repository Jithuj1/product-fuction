# lib imports
from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):

    """
    Allows access only to non authenticated users.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class HasPermission(BasePermission):

    def has_permission(self, request, view):

        if not super().has_permission(request, view):
            return False

        if request.user.is_superuser:
            return True
        
        # If all permission satisfied then only return True
        if hasattr(view, 'permission_dict'):
            group_permissions = [perm.split(".")[1] for perm in request.user.get_all_permissions()]
            permission_list = view.permission_dict.get(request.method, [])
            return all(item in list(group_permissions) for item in permission_list)
        
        # If any permission satisfied then return True
        elif hasattr(view, 'permission_dict_or'):
            group_permissions = [perm.split(".")[1] for perm in request.user.get_all_permissions()]
            permission_list = view.permission_dict_or.get(request.method, [])
            return any(item in list(group_permissions) for item in permission_list)
        
        return False