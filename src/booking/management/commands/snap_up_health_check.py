from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from basis.logger import log


def count_lines(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return len(lines)


def clear_log(filename: str):
    with open(filename, 'w') as file:
        file.write('')


LOG_PATH = '/src/logs/django.log'
MIN_LINES = 500


class Command(BaseCommand):
    help = 'Check the health of the application'

    def handle(self, *args, **options):
        if count_lines(LOG_PATH) > MIN_LINES:
            clear_log(LOG_PATH)
            log.info('Snap up health check: OK')
            return

        send_mail(
            subject='Snap Up THSR 工作排程警告',
            message='Snap Up THSR 的工作排程已久無運作，記得去檢查一下！',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['arcade0425@gmail.com'],
        )
