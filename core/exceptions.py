"""
Custom exception handler for Django REST Framework.
Ensures error responses are formatted as JSON objects instead of JSON lists.
"""

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps list-based error responses into a dict
    with a 'detail' key so all API errors return JSON objects.
    """
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, list):
            if len(response.data) == 1:
                response.data = {"detail": response.data[0]}
            else:
                response.data = {"detail": response.data}

    return response
