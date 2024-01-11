import signal
import time
import traceback
from datetime import timedelta as td

from basis.conf import CURRENT_TZ
from basis.constants import Time
from basis.logger import log
from booking.models import BookingRequest as BR
from booking.tasks import booking_task
from django.core.management.base import BaseCommand
from django.utils import timezone as tz


class SignalMark:
    _instance = None
    cleanup = False


def sigterm_handler(*args):  # ignore signum and frame
    log.info('SIGTERM received, cleanup!!!')
    SignalMark.cleanup = True


signal.signal(signal.SIGTERM, sigterm_handler)


def take_a_break():
    now = tz.now().astimezone(CURRENT_TZ)
    next_day = (now + td(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_diff = (next_day - now).total_seconds()

    if time_diff < Time.ONE_MINUTE:
        time.sleep(time_diff)
    else:
        time.sleep(Time.ONE_MINUTE)


def book_all_pending_reqests():
    pending_requests = BR.get_all_by_status(BR.Status.PENDING)
    for request in pending_requests:
        # Perform the task.booking job on the request
        booking_task(request)


class Command(BaseCommand):
    def handle(self, *args, **options):
        while not SignalMark.cleanup:
            try:
                book_all_pending_reqests()
                take_a_break()

            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                time.sleep(Time.ONE_MINUTE)
