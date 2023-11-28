from django.conf import settings
from pytz import timezone

CURRENT_TZ = timezone(settings.TIME_ZONE)
