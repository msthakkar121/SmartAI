__author__ = "Mohit Thakkar"

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .utils import insert_initial_data


class RationConfig(AppConfig):
    name = 'ration'

    def ready(self):
        post_migrate.connect(insert_initial_data, sender=self)
