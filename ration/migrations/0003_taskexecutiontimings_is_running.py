# Generated by Django 3.0.7 on 2020-10-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration', '0002_auto_20201027_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskexecutiontimings',
            name='is_running',
            field=models.BooleanField(default=False, verbose_name='Is Task Running'),
        ),
    ]
