from django.core.management.base import BaseCommand
from knight.db_scripts.fetch_new_requirements import FetchNewRequirements
from datetime import datetime


# python manage.py fetch_new_requirements

class Command(BaseCommand):
    help = """
    Command to fetch new requirements from the database
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        obj = FetchNewRequirements()
        obj.fetch_new_requirements()
        return
