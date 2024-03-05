import logging
import signal
import traceback
from datetime import time
from time import sleep

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
    if now.time() < time(0, 3):
        tasks.update_not_yet_requests_to_pending()


def take_a_break():
    now = tz.now().astimezone(CURRENT_TZ)
    now_time = now.time()
    if now_time < time(0, 30):
        sleep(Time.FIFTEEN_SECONDS)
    elif now_time < time(23, 59):
        sleep(Time.ONE_MINUTE)
    else:
        time_diff = Time.ONE_MINUTE - now_time.second
        sleep(time_diff)


class Command(BaseCommand):
    def handle(self, *args, **options):
        while not SignalMark.cleanup:
            try:
                log.info('Start snap up')
                switch_requests_status()
                tasks.book_all_pending_reqests()
                tasks.expire_pending_requests()
                log.info('Snap up fininshed, take a break')
                take_a_break()

            except Exception as e:
                log.error(e)
                log.error(traceback.format_exc())
                sleep(Time.ONE_MINUTE)
