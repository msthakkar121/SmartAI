__author__ = "Mohit Thakkar"

from django.apps import AppConfig


class CommanderConfig(AppConfig):
    name = 'commander'

    def ready(self):
        pass
