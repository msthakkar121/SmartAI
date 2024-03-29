__author__ = "Mohit Thakkar"

from django.contrib import admin
from ration.models import TaskExecutionTimings


# Register your models here.

class TaskExecutionTimingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'last_execution_time', 'is_running', 'is_waiting')


admin.site.register(TaskExecutionTimings, TaskExecutionTimingsAdmin)
