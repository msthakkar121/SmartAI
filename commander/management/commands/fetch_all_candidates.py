from django.core.management.base import BaseCommand
from knight.db_scripts.fetch_all_candidates import FetchALlCandidates
from datetime import datetime


# python manage.py fetch_all_candidates

class Command(BaseCommand):
    help = """
    Command to fetch all the candidates in bulk from the database
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # print('Fetching All Commands...\nYet to be implemented...\nPlease check later...')
        print(datetime.now())
        obj = FetchALlCandidates()
        obj.fetch_all_candidates()
        print(datetime.now())
        return
