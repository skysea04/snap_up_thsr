#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

source /etc/environment >> /src/logs/cron.log 2>&1
cd /src
python manage.py snap_up_health_check >> /src/logs/cron.log 2>&1
