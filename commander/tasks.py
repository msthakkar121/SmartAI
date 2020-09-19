__author__ = "Mohit Thakkar"

import sys, traceback

from django.conf import settings
from django.core import management
from django.core.mail import send_mail
from datetime import datetime

from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from knight.db_scripts import logger

celery_logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_test",
    ignore_result=True
)
def task_test():
    """
    Test task
    """
    try:
        print('Test task that runs every minute!!!')
        # management.call_command('fetch_all_candidates')
        # celery_logger.info("Test task printed time!")
    except Exception:
        ex_type, ex, tb = sys.exc_info()
        e = str(traceback.format_exception(ex_type, ex, tb))
        print(e)
        logger.log('(' + str(datetime.now()) + ') ERROR: ' + str(ex))
        send_mail("ERROR in Task_Test", e, settings.EMAIL_HOST, settings.EMAIL_RECIPIENTS)
    return
