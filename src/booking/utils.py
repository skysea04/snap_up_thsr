from datetime import datetime, timedelta as td

from basis.constants import WeekDay

from .constants.bookings import AVAILABLE_DAYS_AFTER_BOOKING


def recognize_img(img: bytes) -> str:
    # You need to find your own way~~~
    return '1234'


def last_can_booking_date(depart_date: datetime):
    can_booking_date = depart_date - td(days=AVAILABLE_DAYS_AFTER_BOOKING)
    if depart_date.weekday() in (WeekDay.Sunday, WeekDay.Saturday):
        left_day = depart_date.weekday() - WeekDay.Friday
        can_booking_date -= td(days=left_day)

    return can_booking_date
