__author__ = "Mohit Thakkar"

from django.contrib import admin
from ration.models import TaskExecutionTimings, Requirements

# Register your models here.

admin.site.register(TaskExecutionTimings)
admin.site.register(Requirements)
