from drf_spectacular.utils import  OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from iam.models import IamUser
from iam.utils import decode_token


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        delattr(request, "user")
        if auth_header := request.headers.get("Authorization"):
            if auth_header.startswith("Bearer"):
                token = auth_header.split(" ")[1]
                try:
                    user_id = decode_token(token)
                    request.iam_user = IamUser.objects.get(id=user_id)
                except:
                    pass

        return self.get_response(request)


