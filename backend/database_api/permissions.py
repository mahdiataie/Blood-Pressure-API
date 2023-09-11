from rest_framework.permissions import BasePermission

class IsHouseholdOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow admins to see everything
        if request.user and request.user.is_staff:
            return True

        # Restrict other users to their own data
        uuid = request.query_params.get('uuid')
        if not uuid:
            return False

        return request.user.uuid == uuid