from datetime import datetime
from django.utils.timezone import make_aware


def insert_initial_data(sender, **kwargs):
    from ration.models import TaskExecutionTimings
    TaskExecutionTimings.objects.get_or_create(task_name='GetCandidateDetails',
                                               last_execution_time=make_aware(datetime.now()))
    TaskExecutionTimings.objects.get_or_create(task_name='GetRequirementDetails',
                                               last_execution_time=make_aware(datetime.now()))
