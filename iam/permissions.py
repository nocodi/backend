from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from iam.models import IamUser
class IsLoginedPermission(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request, 'iam_user') and isinstance(request.iam_user, IamUser):
            return True
        raise PermissionDenied("token is absent or invalid")
