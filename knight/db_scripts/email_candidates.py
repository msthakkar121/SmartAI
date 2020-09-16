__author__ = "Mohit Thakkar"

import pyodbc
from django.conf import settings


class EmailCandidates:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def email_candidates(self, requirement_id, candidate_ids, scores):
        with self.connection.cursor() as cursor:
            cursor.execute("{CALL usp_ML_I_ResumeMatch2 (?,?,?)}", (requirement_id, candidate_ids, scores))
