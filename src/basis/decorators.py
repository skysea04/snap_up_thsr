import traceback
from functools import wraps

from pydantic import BaseModel, ValidationError

from django.http import HttpRequest, JsonResponse

from . import error_codes, messages
from .exceptions import AppException
from .logger import log


def response_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return JsonResponse(res)

        except AppException as e:
            log.error('APP_ERROR | msg: %s', e.msg)
            res = {
                'error': e.msg,
                'code': e.code
            }
            return JsonResponse(res, status=e.status_code)

        except Exception as e:
            log.error('SERVER_ERROR | msg: %s', e)
            log.error(traceback.format_exc())
            res = {
                'error': messages.SERVER_ERROR,
                'code': 1,
            }
            return JsonResponse(res, status=500)

    return wrapper


def parse_request_body(param_model: BaseModel):
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            try:
                data = param_model.model_validate_json(request.body)
            except ValidationError as e:
                log.error('BAD_REQUEST | msg: %s', e)
                raise AppException(
                    msg=messages.BAD_REQUEST,
                    status_code=400,
                    code=error_codes.CODE__PARSE_PARAM_ERROR,
                ) from e

            return func(request, data=data, *args, **kwargs)

        return wrapper
    return decorator
