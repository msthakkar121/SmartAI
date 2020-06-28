import os

import pyodbc
from django.conf import settings

# Get directory for 'Knight'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FetchALlCandidates:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_all_candidates(self):
        return
