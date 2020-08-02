__author__ = "Mohit Thakkar"

from django.core.management.base import BaseCommand
from knight.py_scripts.fetch_skills import FetchSkills


# python manage.py fetch_skills

class Command(BaseCommand):
    help = """
    Command to fetch all the recorded skills from the database
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        obj = FetchSkills()
        obj.fetch_skills()
        return
