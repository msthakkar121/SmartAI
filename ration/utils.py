__author__ = "Mohit Thakkar"

from datetime import datetime
from django.utils.timezone import make_aware


def insert_initial_data(sender, **kwargs):
    from ration.models import TaskExecutionTimings

    obj, created = TaskExecutionTimings.objects.get_or_create(task_name='GetCandidateDetails')
    if created:
        obj.last_execution_time=make_aware(datetime.now())
        obj.save()

    obj, created = TaskExecutionTimings.objects.get_or_create(task_name='GetRequirementDetails')
    if created:
        obj.last_execution_time=make_aware(datetime.now())
        obj.save()
