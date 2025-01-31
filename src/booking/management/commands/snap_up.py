import logging
import traceback

from django.core.management.base import BaseCommand

from basis.logger import log
from booking import tasks

log.addHandler(logging.StreamHandler())


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tasks.update_not_yet_requests_to_pending()
            tasks.book_all_pending_requests()

        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
