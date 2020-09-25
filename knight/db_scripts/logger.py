__author__ = "Mohit Thakkar"

import pyodbc
from django.conf import settings


def log(data):
    connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                SERVER=settings.DB_SERVER,
                                DATABASE=settings.DB_NAME,
                                UID=settings.DB_USER,
                                PWD=settings.DB_PASSWORD)
    with connection.cursor() as cursor:
        cursor.execute("Insert into ProcessLog (Data) VALUES (?)", ('[Artie 2.0] ' + str(data)))

    connection.close()
