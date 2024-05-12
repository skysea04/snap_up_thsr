from datetime import timedelta as td

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone as tz

from booking.models import HolidayInfo
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        tomorrow = tz.localdate() + td(days=1)
        holiday_info = HolidayInfo.get_by_date(tomorrow)
        if not holiday_info:
            return

        for user in User.need_remind_list():
            send_mail(
                subject=f'台灣高鐵 {holiday_info.name} 疏運期間訂票提醒',
                message='',
                html_message='<br/>'.join([
                    f'明天 ({tomorrow}) 是高鐵 {holiday_info.name} 疏運期間 ({holiday_info.adjust_period}) 開放訂票日，',
                    '可以先前往 <a href="https://thsr.yhchiu.com/admin/booking/bookingrequest/">系統</a> 預約訂票喔！',
                    '',
                    '--------------------------------',
                    '',
                    f'若不想收到訂票提醒，可前往 <a href="https://thsr.yhchiu.com/admin/user/user/{user.pk}/change/">個人頁面<a/> 將「疏運節日訂票提醒」取消勾選'
                ]),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
