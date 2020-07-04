import os
import pandas as pd
from datetime import datetime
from django.utils.timezone import make_aware

from knight.db_scripts.fetch_new_requirements import FetchNewRequirements as FNR
from ration.models import TaskExecutionTimings

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchNewRequirements:
    def __init__(self):
        pass

    def fetch_new_requirements(self):
        # Get last executed time for the task
        obj = TaskExecutionTimings.objects.get(task_name='GetRequirementDetails')
        last_executed_time = obj.last_execution_time.replace(tzinfo=None, microsecond=0)
        now = datetime.now().replace(tzinfo=None, microsecond=0)

        fnr = FNR()
        df = fnr.fetch_new_requirements()

        obj.last_execution_time = make_aware(datetime.now())
        obj.save()

        print(df)
        print('\n\nFetched ', len(df), ' new requirements from ', last_executed_time, ' to ', now)

        pass
