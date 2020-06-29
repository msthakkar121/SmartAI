import os
from datetime import datetime

import pyodbc
from django.conf import settings

import pandas as pd
from ration.models import TaskExecutionTimings

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchNewRequirements:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_new_requirements(self):
        # Get last executed time for the task
        obj = TaskExecutionTimings.objects.get(task_name='GetRequirementDetails')
        last_executed_time = obj.last_execution_time.replace(tzinfo=None, microsecond=0)
        now = datetime.now().replace(tzinfo=None, microsecond=0)

        query = """
                SELECT  
                    rm.RequirementID,
                    jtm.JobTitleText AS JobTitle,
                    jtm2.JobTypeText AS JobType,
                    rm.IsRemoteLocation,
                    vm.VisaName AS VisaStatus,
                    rm.RequirementJobDescription,
                    rm.ActualRequirement,
                    reverse(stuff(reverse(CONCAT(
                        CASE
                        WHEN rs.MandatorySkill1 IS NULL
                            THEN ''
                            ELSE rs.MandatorySkill1 + ', '
                        END,
                        CASE
                        WHEN rs.MandatorySkill2 IS NULL
                            THEN ''
                            ELSE rs.MandatorySkill2 + ', '
                        END,
                        CASE
                        WHEN rs.MandatorySkill3 IS NULL
                            THEN ''
                            ELSE rs.MandatorySkill3 + ', '
                        END,
                        CASE
                        WHEN rs.MandatorySkill4 IS NULL
                            THEN ''
                            ELSE rs.MandatorySkill4 + ', '
                        END)), 1, 2, '')) AS RequirementSkills,
                    Stuff(
                        (SELECT DISTINCT ', ' +zm.ZIPCode
                        FROM dbo.RequirementMaster rm2
                        LEFT JOIN dbo.RequirementLocation rl ON rm2.RequirementID = rl.RequirementID
                        LEFT JOIN dbo.RequirementOtherLocation rol ON rm2.RequirementID = rol.RequirementID			
                        LEFT JOIN dbo.AddressMaster am ON rl.AddressID = am.AddressID OR rol.AddressID = am.AddressID
                        LEFT JOIN dbo.ZIPCodeMaster zm ON  am.ZIPCodeID = zm.ZIPCodeID
                        WHERE rm.RequirementID = rm2.RequirementID  for xml path ('')),1,1,'') AS RequirementZIPCode,
                    rm.CreatedDate,
                    rm.ModifiedDate
                FROM
                    dbo.RequirementMaster rm
                LEFT JOIN
                    dbo.JobTitleMaster jtm ON rm.JobTitleID = jtm.JobTitleID
                LEFT JOIN
                    dbo.JobTypeMaster jtm2 ON rm.JobTypeID = jtm2.JobTypeID
                LEFT JOIN 
                    dbo.RequirementVisa rv ON rm.RequirementID = rv.RequirementID
                LEFT JOIN
                    dbo.VisaMaster vm ON rv.VisaID = vm.VisaID
                LEFT JOIN
                    dbo.RequirementSkill rs ON rm.RequirementID = rs.RequirementID
                WHERE
                    rm.CreatedDate > '{0}'
        """.format(last_executed_time)

        df = pd.read_sql_query(query, self.connection)
        print(df)

        print('\n\nFetched ', len(df), ' new requirements from ', last_executed_time, ' to ', now)
        return
