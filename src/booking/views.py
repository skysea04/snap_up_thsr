from datetime import datetime as dt, timedelta as td
from typing import Dict

from basis.conf import CURRENT_TZ
from basis.constants import Time
from basis.decorators import parse_request_body
from basis.exceptions import AppException
from django.http import HttpRequest
from django.utils import timezone as tz
from django.views.decorators.http import require_GET, require_POST
from user.decorators import check_login
from user.models import User

from . import error_codes, exceptions, messages, utils
from .constants.bookings import MAX_TICKET_NUM, AvailableTime, PassengerNum, Station
from .models import BookingRequest
from .param_models import BookingRequestParam
from .tasks import booking_task

# @require_GET
# def test_task(request: HttpRequest, **kwargs):
#     after_3_sec = tz.now() + td(seconds=3)
#     add.apply_async((1, 2), eta=after_3_sec)
#     return {}


@require_GET
@check_login
def booking_request_choices(request: HttpRequest, **kwargs):
    return {
        'station_choices': Station.choices,
        'passenger_num_choices': PassengerNum.choices,
        'avilable_time_choices': AvailableTime.choices,
    }


@require_POST
@check_login
@parse_request_body(BookingRequestParam)
def create_booking_request(request: HttpRequest, user: User, data: BookingRequestParam) -> Dict:
    if not 1 <= data.total_num <= MAX_TICKET_NUM:
        raise AppException(
            msg=messages.ERROR__TICKET_NUM,
            code=error_codes.CODE__WRONG_TICKET_NUM,
            status_code=400,
        )

    booking_request = BookingRequest(
        user_email=user.email,
        depart_station=data.depart_station,
        dest_station=data.dest_station,
        adult_num=data.adult_num,
        child_num=data.child_num,
        disabled_num=data.disabled_num,
        elder_num=data.elder_num,
        college_num=data.college_num,
        depart_date=data.depart_date,
        earliest_depart_time=data.earliest_depart_time,
        latest_arrival_time=data.latest_arrival_time,
    )

    booking_request.save()

    depart_date = dt.strptime(data.depart_date, '%Y-%m-%d').replace(tzinfo=CURRENT_TZ)
    last_can_booking_date = utils.last_can_booking_date(depart_date)

    # booking_task(booking_request)

    return {
        'id': booking_request.pk
    }
