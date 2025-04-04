from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from iam.models import IamUser


class IsLoginedPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if hasattr(request, "iam_user") and isinstance(request.iam_user, IamUser):
            return True
        raise NotAuthenticated("token is absent or invalid")
