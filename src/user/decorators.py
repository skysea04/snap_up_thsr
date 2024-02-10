from django.http import HttpRequest

from basis import messages
from basis.exceptions import AppException
from basis.logger import log

from . import error_codes
from .models import User


def check_login(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        uid = request.session.get('uid')
        if not uid:
            raise AppException(
                msg=messages.UNAUTHORIZED,
                code=error_codes.CODE__NO_SESSION,
                status_code=401
            )

        user = User.get(uid)
        if not user:
            del request.session['uid']
            log.error('User of session not found, uid: %s', uid)
            raise AppException(
                msg=messages.UNAUTHORIZED,
                code=error_codes.CODE__NO_USER,
                status_code=401,
            )

        return func(request, user=user, *args, **kwargs)

    return wrapper
