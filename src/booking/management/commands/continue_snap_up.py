import logging
import signal
import time
import traceback
from datetime import timedelta as td

from basis.conf import CURRENT_TZ
from basis.constants import Time
from basis.logger import log
from booking import tasks
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone as tz

if settings.DEV_MODE:
    log.addHandler(logging.StreamHandler())


class SignalMark:
    _instance = None
    cleanup = False


def sigterm_handler(*args):  # ignore signum and frame
    log.info('SIGTERM received, cleanup!!!')
    SignalMark.cleanup = True


signal.signal(signal.SIGTERM, sigterm_handler)


def switch_requests_status():
    now = tz.now().astimezone(CURRENT_TZ)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if (now - today).total_seconds() <= Time.TEN_MINUTES:
        tasks.update_not_yet_requests_to_pending()


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
                switch_requests_status()
                tasks.expire_pending_requests()
                tasks.book_all_pending_reqests()
                take_a_break()

            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                time.sleep(Time.ONE_MINUTE)
