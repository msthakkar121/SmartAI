__author__ = "Mohit Thakkar"

from django.db import models
from datetime import datetime


# Create your models here.


class TaskExecutionTimings(models.Model):
    # The first element in each tuple is the value that will be stored in the database.
    # The second element is displayed by the field’s form widget.
    task_names = [
        ('GetCandidateDetails', 'Get Candidate Details'),
        ('GetRequirementDetails', 'Get Requirement Details'),
        ('ProcessRequirements', 'Process Requirements'),
    ]

    task_name = models.CharField(max_length=100, choices=task_names, unique=True, null=False)
    last_execution_time = models.DateTimeField(default=datetime.now,
                                               help_text='The created/updated time for the last record fetched by the task.')

    class Meta:
        verbose_name = "TaskExecutionTiming"
        verbose_name_plural = "TaskExecutionTimings"


class Requirements(models.Model):
    STATUS = [
        (0, 'PENDING'),
        (1, 'COMPLETED'),
        (2, 'ERROR')
    ]

    requirement_id = models.TextField('RequirementID', unique=True, null=True, blank=True)
    job_title = models.TextField('JobTitle', null=True, blank=True)
    job_type = models.TextField('JobType', null=True, blank=True)
    is_remote_location = models.TextField('IsRemoteLocation', null=True, blank=True)
    visa_status = models.TextField('VisaStatus', null=True, blank=True)
    requirement_job_description = models.TextField('RequirementJobDescription', null=True, blank=True)
    actual_requirement = models.TextField('ActualRequirement', null=True, blank=True)
    requirement_skills = models.TextField('RequirementSkills', null=True, blank=True)
    requirement_zip_code = models.TextField('RequirementZIPCode', null=True, blank=True)
    created_date = models.DateTimeField('CreatedDate', null=True, blank=True)
    modified_date = models.DateTimeField('ModifiedDate', null=True, blank=True)
    status = models.SmallIntegerField('RequirementStatus', choices=STATUS, default=0)

    class Meta:
        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"
