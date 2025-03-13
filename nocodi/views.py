from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class LivenessView(APIView):
    """
    A simple view that returns 200 OK to indicate the service is alive
    """

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})
