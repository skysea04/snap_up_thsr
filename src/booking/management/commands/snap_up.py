import logging
import traceback

from basis.logger import log
from booking import tasks
from django.core.management.base import BaseCommand

log.addHandler(logging.StreamHandler())


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tasks.update_not_yet_requests_to_pending()
            tasks.book_all_pending_reqests()

        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
