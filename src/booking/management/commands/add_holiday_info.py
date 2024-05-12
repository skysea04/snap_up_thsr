from datetime import datetime
import logging
import re
import requests

from bs4 import BeautifulSoup, Tag
from django.core.management.base import BaseCommand

from basis.logger import log
from booking.models import HolidayInfo


INFO_URL = 'https://www.thsrc.com.tw/ArticleContent/60dbfb79-ac20-4280-8ffb-b09e7c94f043'


class Command(BaseCommand):
    def handle(self, *args, **options):
        log.addHandler(logging.StreamHandler())

        try:
            HolidayInfo.clear_old_infos()

            resp = requests.get(INFO_URL)
            page = BeautifulSoup(resp.text, 'html.parser')
            holiday_info_rows: list[Tag] = (
                page.find('div', {'class': 'news'})
                .find('table', {'class': 'table'})
                .find_all('tr')
            )

            for row in holiday_info_rows:
                cols: list[Tag] = row.find_all('td')

                if len(cols) != 3:  # should have 3 columns
                    continue

                holiday_name = cols[0].text
                adjust_period = cols[1].text
                str_start_reverse_date = re.search(r'\d{4}/\d{2}/\d{2}', cols[2].text).group()
                start_reverse_date = datetime.strptime(str_start_reverse_date, '%Y/%m/%d').date()

                if HolidayInfo.holiday_exist(start_reverse_date):
                    continue

                HolidayInfo.objects.create(
                    name=holiday_name,
                    adjust_period=adjust_period,
                    start_reserve_date=start_reverse_date
                )

        except Exception as e:
            log.error('Failed to get holiday reservation start date | error: %s', e)
