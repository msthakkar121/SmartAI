from _datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings


# python manage.py fetch_all_candidates

class Command(BaseCommand):
    help = """
    Command to fetch all the candidates in bulk from the database
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print('Fetching All Commands...\nYet to be implemented...\nPlease check later...')
        pass
