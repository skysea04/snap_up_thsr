import traceback
import uuid

from basis.logger import log
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from user.models import InviteCode


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--num',
            default=10,
            type=int,
            help='how many invite code will be generated',
        )

    def handle(self, *args, **options):
        code_set = set()
        for _ in range(options['num']):
            code = uuid.uuid4().hex[:8]
            while code in code_set:
                code = uuid.uuid4().hex[:8]

            try:
                InviteCode.create(code)

            except IntegrityError as e:
                log.error('Duplicate Code')
                log.error(log.error(traceback.print_exc(e)))

            except Exception as e:
                log.error(log.error(traceback.print_exc(e)))
