# Generated by Django 3.0.7 on 2020-10-26 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ration', '0003_auto_20201026_1422'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requirements',
            options={'verbose_name': 'Requirement', 'verbose_name_plural': 'Requirements'},
        ),
        migrations.AlterModelOptions(
            name='taskexecutiontimings',
            options={'verbose_name': 'TaskExecutionTiming', 'verbose_name_plural': 'TaskExecutionTimings'},
        ),
        migrations.AlterModelTable(
            name='requirements',
            table=None,
        ),
        migrations.AlterModelTable(
            name='taskexecutiontimings',
            table=None,
        ),
    ]