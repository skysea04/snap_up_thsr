import os
import sys
from datetime import datetime, timedelta as td

import ddddocr
from basis.constants import WeekDay

from .constants.bookings import AVAILABLE_DAYS_AFTER_BOOKING

# Initial ocr, initial process will print advertising text, redirect the text to null
sys.stdout = open(os.devnull, 'w')
img_ocr = ddddocr.DdddOcr()
sys.stdout = sys.__stdout__


def recognize_img(img: bytes) -> str:
    return img_ocr.classification(img)


def last_can_booking_date(depart_date: datetime):
    can_booking_date = depart_date - td(days=AVAILABLE_DAYS_AFTER_BOOKING)
    if depart_date.weekday() in (WeekDay.Sunday, WeekDay.Saturday):
        left_day = depart_date.weekday() - WeekDay.Friday
        can_booking_date -= td(days=left_day)

    return can_booking_date
