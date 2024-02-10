from pytz import timezone

from django.conf import settings

CURRENT_TZ = timezone(settings.TIME_ZONE)
