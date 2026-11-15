from rest_framework.permissions import BasePermission


class IsActivePortalStaff(BasePermission):
    """Allow active ADC staff and admins to use staff portal APIs."""

    message = 'Active staff portal access is required.'

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.role in {'staff', 'admin'}
        )


class IsActivePortalAdmin(IsActivePortalStaff):
    """Allow active admin-role users to manage portal users."""

    message = 'Active portal administrator access is required.'

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'admin'
