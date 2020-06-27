from django.db import models
from django.utils import timezone


# Create your models here.


class TaskExecutionTimings(models.Model):
    # The first element in each tuple is the value that will be stored in the database.
    # The second element is displayed by the field’s form widget.
    task_names = [
        ('GetCandidateDetails', 'Get Candidate Details'),
        ('GetRequirementDetails', 'Get Requirement Details'),
    ]

    task_name = models.CharField(max_length=100, choices=task_names, unique=True, null=False)
    last_execution_time = models.DateTimeField(default=timezone.now,
                                               help_text='The created/updated time for the last record fetched by the task.')

    class Meta:
        db_table = "TaskExecutionTimings"
