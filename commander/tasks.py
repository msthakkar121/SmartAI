import time
from datetime import datetime

from django.core import management

from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_test",
    ignore_result=True
)
def task_test():
    """
    Print message
    """
    
    management.call_command('fetch_all_candidates')
    # logger.info("Test task printed time!")
    return
