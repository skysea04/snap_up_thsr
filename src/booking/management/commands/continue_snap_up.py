import logging
import signal
import traceback
from datetime import time
from datetime import timedelta as td
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone as tz

from basis.constants import Time
from basis.logger import log
from booking import tasks

if settings.DEV_MODE:
    log.addHandler(logging.StreamHandler())


class SignalMark:
    _instance = None
    cleanup = False


def sigterm_handler(*args):  # ignore signum and frame
    log.info("SIGTERM received, cleanup!!!")
    SignalMark.cleanup = True


signal.signal(signal.SIGTERM, sigterm_handler)


def switch_requests_status():
    now = tz.localtime()
    if now.time() < time(0, 3):
        tasks.update_not_yet_requests_to_pending()


def take_a_break(all_success: bool, in_maintenance: bool):
    now = tz.localtime()
    next_day = now.replace(hour=0, minute=0, second=0) + td(days=1)
    time_diff = (next_day - now).seconds

    if in_maintenance:
        sleep(min(time_diff, Time.TEN_MINUTES))
    else:
        if all_success:
            sleep(min(Time.ONE_MINUTE, time_diff))
        else:
            sleep(Time.FIFTEEN_SECONDS)


class Command(BaseCommand):
    def handle(self, *args, **options):
        while not SignalMark.cleanup:
            try:
                log.info("Start snap up")
                switch_requests_status()
                all_success, in_maintenance = tasks.book_all_pending_requests()
                tasks.expire_pending_requests()
                log.info("Snap up finished, take a break")
                take_a_break(all_success, in_maintenance)

            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                sleep(Time.ONE_MINUTE)
