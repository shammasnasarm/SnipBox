import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class CommonResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """
        Wrap all responses in a common structure.
        {
            "success": bool,
            "message": str,
            "data": object | null,
            "errors": object | null
        }
        """
        if isinstance(response, Response):
            data = response.data
            status_code = response.status_code
        else:
            try:
                data = json.loads(response.content.decode('utf-8'))
            except Exception:
                return response
            status_code = response.status_code

        success = 200 <= status_code < 400

        wrapped = {
            "success": success,
            "message": "Request processed successfully"
            if success else "Request failed",
            "data": data if success else None,
            "errors": None if success else data,
        }

        return JsonResponse(wrapped, status=status_code)

    def process_exception(self, request, exception):
        """Handle uncaught exceptions globally."""
        return JsonResponse({
            "success": False,
            "message": str(exception),
            "errors": {"detail": str(exception)},
        }, status=500)
