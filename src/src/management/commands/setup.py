import glob

from django.core.management import call_command
from django.core.management.base import BaseCommand


def find_all_fixtures(wildcard: str) -> list[str]:
    return glob.glob(wildcard, recursive=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('loaddata', *find_all_fixtures('*/fixtures/*'))
