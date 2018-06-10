from __future__ import absolute_import
from movies import settings

from rest_framework.response import Response

ERROR_CODES = {
    "IMDV000": "Internal Server Error",
    "IMBD100": "User Doesnot Exists",
    "IMDB101": "User Already Registered with this username",
    "IMDB102": "Invalid reference_no. Please provide correct reference_no",
    "IMDB103": "Invalid username provided",
    "IMDB105": "Invalid admin_reference_no provided.",
    "IMDB106": "Invalid role provided."
}


class UserAlreadyExists(Exception):
    pass


class AdminAccessException(Exception):
    pass


def make_exc_response(
        request, error_code, status_code, excpetion=None, reason=""):
    response = {
        "success": False,
        "error_code": error_code,
        "error_message": (
            str(excpetion) if settings.DEBUG and status_code == 500 and excpetion else ERROR_CODES[error_code] + reason  # noqa
        )
    }
    if request.data.get('reference_no'):
        response['reference_no'] = request.data.get('reference_no')
    elif request.data.get('admin_reference_no'):
        response['admin_reference_no'] = request.data.get('admin_reference_no')
    else:
        response['reference_no'] = "Invalid"
    return Response((response), status=status_code)


def make_success_response(request, data, status):
    data.update({
        "success_message": "Request processed successfully!"
    })
    if request.data.get('reference_no'):
        data['reference_no'] = request.data.get('reference_no')
    elif request.data.get('admin_reference_no'):
        data['admin_reference_no'] = request.data.get('admin_reference_no')
    else:
        data['reference_no'] = "Invalid"
    return Response(data, status)
