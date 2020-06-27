# Generated by Django 3.0.7 on 2020-06-26 12:18

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskExecutionTimings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(choices=[('GetCandidateDetails', 'Get Candidate Details'), ('GetRequirementDetails', 'Get Requirement Details')], max_length=100, unique=True)),
                ('last_execution_time', models.DateTimeField(default=django.utils.timezone.now, help_text='The created/updated time for the last record fetched by the task.')),
            ],
            options={
                'db_table': 'TaskExecutionTimings',
            },
        ),
    ]
