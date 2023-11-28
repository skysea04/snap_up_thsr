import traceback

from django.conf import settings
from django.http import JsonResponse

from . import error_codes, messages
from .exceptions import AppException
from .logger import log


class ResponseHandleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, dict):
            return JsonResponse(response)

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, AppException):
            log.error('APP_ERROR | msg: %s', exception.msg)
            res = {
                'error': exception.msg,
                'code': exception.code
            }
            return JsonResponse(res, status=exception.status_code)

        if settings.DEV_MODE:
            raise exception

        # unhandled exceptions
        log.error('SERVER_ERROR | msg: %s', exception)
        log.error(traceback.format_exc())
        res = {
            'error': messages.SERVER_ERROR,
            'code': error_codes.CODE__UNHANDLED_ERROR,
        }
        return JsonResponse(res, status=500)
