import logging
import signal
import time
import traceback
from datetime import timedelta as td

from django.core.management.base import BaseCommand
from django.utils import timezone as tz

from basis.conf import CURRENT_TZ
from basis.constants import Time
from basis.logger import log
from booking import tasks

log.addHandler(logging.StreamHandler())


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


class Command(BaseCommand):
    def handle(self, *args, **options):
        while not SignalMark.cleanup:
            try:
                tasks.update_not_yet_requests_to_pending()
                tasks.book_all_pending_reqests()
                take_a_break()

            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                time.sleep(Time.ONE_MINUTE)
