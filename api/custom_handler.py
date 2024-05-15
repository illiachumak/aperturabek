# custom_exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)
    if response and (response.status_code == 500 or response.status_code == 405):
        response.status_code = 404
        response.data = {'detail': 'Not found'}

    return response

