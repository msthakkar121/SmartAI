# Generated by Django 3.0.7 on 2020-06-27 06:19

import datetime
from django.db import migrations, models


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
                ('last_execution_time', models.DateTimeField(default=datetime.datetime.now, help_text='The created/updated time for the last record fetched by the task.')),
            ],
            options={
                'db_table': 'TaskExecutionTimings',
            },
        ),
    ]
