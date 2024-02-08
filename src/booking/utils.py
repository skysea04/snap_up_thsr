import os
import sys
import traceback
from datetime import date, datetime as dt, timedelta as td

import ddddocr
import requests
from basis.cache import expire_cache
from basis.constants import Time, WeekDay
from basis.logger import log

from .constants import bookings, urls

# Initial ocr, initial process will print advertising text, redirect the text to null
sys.stdout = open(os.devnull, 'w')
img_ocr = ddddocr.DdddOcr()
sys.stdout = sys.__stdout__


def recognize_img(img: bytes) -> str:
    return img_ocr.classification(img)


def last_can_booking_date(depart_date: dt):
    can_booking_date = depart_date - td(days=bookings.AVAILABLE_DAYS_AFTER_BOOKING)
    if depart_date.weekday() in (WeekDay.Sunday, WeekDay.Saturday):
        left_day = depart_date.weekday() - WeekDay.Friday
        can_booking_date -= td(days=left_day)

    return can_booking_date


@expire_cache(seconds=Time.ONE_DAY, refresh_on_new_day=True)
def get_latest_booking_date() -> date:
    today_date = date.today()
    try:
        res = requests.get(urls.LATEST_BOOKING_DATE.format(today_date=today_date.strftime('%Y%m%d'))).content.decode()

        return dt.strptime(res, '%Y/%m/%d').date()

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())

    latest_booking_date = today_date + td(days=bookings.AVAILABLE_DAYS_AFTER_BOOKING)
    if latest_booking_date.weekday() in (WeekDay.Friday, WeekDay.Saturday):
        left_day = WeekDay.Sunday - latest_booking_date.weekday()
        latest_booking_date += td(days=left_day)

    return latest_booking_date
