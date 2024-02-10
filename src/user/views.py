from typing import Dict

from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.views.generic import View

from basis.decorators import parse_request_body
from basis.exceptions import AppException
from basis.validators import validate_n_format_phone, validate_personal_id

from . import decorators, error_codes, messages
from .models import InviteCode, User
from .param_models import FillProfile, Login, Signup


@require_GET
@ensure_csrf_cookie
def index(request: HttpRequest):
    return {'msg': 'Hi!'}


@require_POST
@parse_request_body(Signup)
def signup(request: HttpRequest, data: Signup):
    with transaction.atomic():
        invite_code = InviteCode.get_for_update(data.invite_code)
        if not invite_code:
            raise AppException(
                msg=messages.INVALID_INVITE_CODE,
                code=error_codes.CODE__NO_INVITE_CODE,
                status_code=400,
            )

        if invite_code.is_used:
            raise AppException(
                msg=messages.INVALID_INVITE_CODE,
                code=error_codes.CODE__INVITE_CODE_IS_USED,
                status_code=400,
            )

        invite_code.is_used = True
        invite_code.save()
        User.create(
            email=data.email,
            hash_pwd=make_password(data.password),
            code=data.invite_code
        )

    return {}


@require_POST
@parse_request_body(Login)
def login(request: HttpRequest, data: Login) -> Dict:
    user = User.get_by_email(data.email)
    if not user:
        raise AppException(
            msg=messages.ERROR_SIGNIN,
            code=error_codes.CODE__NO_USER,
            status_code=400,
        )

    if not check_password(data.password, user.password):
        raise AppException(
            msg=messages.ERROR_SIGNIN,
            code=error_codes.CODE__WRONG_PWD,
            status_code=400,
        )

    request.session['uid'] = user.pk

    return {}


@require_POST
@decorators.check_login
def logout(request: HttpRequest, **kwargs) -> Dict:
    del request.session['uid']
    return {}


@method_decorator(decorators.check_login, name='dispatch')
class ProfileView(View):
    def get(self, request: HttpRequest, **kwargs):
        print(kwargs['user'])
        return {'ok': True}

    @method_decorator(parse_request_body(FillProfile), name='put')
    def put(self, request: HttpRequest, user: User, data: FillProfile):
        if not validate_personal_id(data.personal_id):
            raise AppException(
                msg=messages.INVALID_PERSONAL_ID,
                code=error_codes.CODE__INVALID_PERSONAL_ID,
                status_code=400,
            )

        formated_phone = validate_n_format_phone(data.phone)
        if not formated_phone:
            raise AppException(
                msg=messages.INVALID_PHONE,
                code=error_codes.CODE__INVALID_PHONE,
                status_code=400,
            )

        user.personal_id = data.personal_id
        user.phone = formated_phone
        user.save(update_fields=['updated_at', 'personal_id', 'phone'])

        return {}
