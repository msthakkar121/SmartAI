__author__ = "Mohit Thakkar"

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
    Test task
    """
    print('Test task that runs every minute!!!')
    # management.call_command('fetch_all_candidates')
    # logger.info("Test task printed time!")
    return
