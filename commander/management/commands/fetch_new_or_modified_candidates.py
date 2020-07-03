from django.core.management.base import BaseCommand
from knight.py_scripts.fetch_new_or_modified_candidates import FetchNewOrModifiedCandidates


# python manage.py fetch_all_candidates

class Command(BaseCommand):
    help = """
    Command to fetch all the candidates in bulk from the database
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        obj = FetchNewOrModifiedCandidates()
        obj.fetch_new_or_modified_candidates()
        return
