__author__ = "Mohit Thakkar"

import pyodbc
import pandas as pd

from django.conf import settings


class FetchSkills:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_skills(self):
        query = """
                SELECT  
                    sm.SkillName
                FROM
                    dbo.SkillMaster sm WITH (NOLOCK)
                ORDER BY
                    sm.SkillName
        """

        df = pd.read_sql_query(query, self.connection)
        df.drop(columns=list(df.filter(regex='Unnamed:')), inplace=True)

        return df
