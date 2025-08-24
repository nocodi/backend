import logging
from typing import Callable

from cachetools import TTLCache
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response

logger = logging.getLogger(__name__)


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


class RatelimitMiddleware:

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.limits = TTLCache(1000, settings.RATE_LIMIT_INTERVAL)

    def __call__(self, request: Request) -> Response:
        client_ip = request.META.get("REMOTE_ADDR")
        if self.limits.get(client_ip, 0) >= settings.RATE_LIMIT_COUNT:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            from django.http import JsonResponse

            return JsonResponse({"detail": "Rate limit exceeded."}, status=429)
        self.limits[client_ip] = self.limits.get(client_ip, 0) + 1
        return self.get_response(request)
