from typing import Callable

from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response


class CacheMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.cache = {}

    def __call__(self, request: Request) -> Response:
        if request.path not in settings.STATIC_CACHE_PATHS:
            return self.get_response(request)

        if request.path not in self.cache:
            res = self.get_response(request)
            self.cache[request.path] = res
        else:
            res = self.cache[request.path]
            res["X-Local-Cache"] = "HIT"
        return res
