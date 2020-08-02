__author__ = "Mohit Thakkar"

from django.core.management.base import BaseCommand
from knight.py_scripts.fetch_new_or_modified_requirements import FetchNewOrModifiedRequirements
from datetime import datetime


# python manage.py fetch_new_or_modified_requirements

class Command(BaseCommand):
    help = """
    Command to fetch new requirements from the database
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        obj = FetchNewOrModifiedRequirements()
        obj.fetch_new_or_modified_requirements()
        return
