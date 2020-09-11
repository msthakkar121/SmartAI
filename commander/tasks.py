__author__ = "Mohit Thakkar"

from django.core import management
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
    except Exception as e:
        logger.log('(' + str(datetime.now()) + ') ERROR: ' + str(e))
    return
