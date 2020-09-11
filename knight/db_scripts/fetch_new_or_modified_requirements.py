__author__ = "Mohit Thakkar"

import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.conf import settings

from ration.models import TaskExecutionTimings


class FetchNewOrModifiedRequirements:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_new_or_modified_requirements(self):
        # Get last executed time for the task
        obj = TaskExecutionTimings.objects.get(task_name='GetRequirementDetails')
        last_executed_time = obj.last_execution_time.replace(tzinfo=None, microsecond=0)
        now = datetime.now().replace(tzinfo=None, microsecond=0)
        start_modified_time = last_executed_time - timedelta(minutes=180)
        end_modified_time = start_modified_time + (now - last_executed_time)

        # CONDITIONS TO CHECK
        #
        # 1. CreatedDate should be after last execution time
        #
        # 2. JobStatus should be OPEN
        #
        # 3. ModifiedDate should be in the slot before 3 hours from last executed time
        #    For example, if you check for requirements every 15 mins ,
        #    and current check time is 3:15, the last execution time must be 3
        #    So the Modified date should be between 12 (3 hours prior to last execution time)
        #    and 12:15 (add the difference between current time & last execution time)

        # query = """
        #         SELECT
        #             rm.RequirementID,
        #             jtm.JobTitleText AS JobTitle,
        #             jtm2.JobTypeText AS JobType,
        #             rm.IsRemoteLocation,
        #             vm.VisaName AS VisaStatus,
        #             rm.RequirementJobDescription,
        #             rm.ActualRequirement,
        #             reverse(stuff(reverse(CONCAT(
        #                 CASE
        #                 WHEN rs.MandatorySkill1 IS NULL
        #                     THEN ''
        #                     ELSE rs.MandatorySkill1 + ', '
        #                 END,
        #                 CASE
        #                 WHEN rs.MandatorySkill2 IS NULL
        #                     THEN ''
        #                     ELSE rs.MandatorySkill2 + ', '
        #                 END,
        #                 CASE
        #                 WHEN rs.MandatorySkill3 IS NULL
        #                     THEN ''
        #                     ELSE rs.MandatorySkill3 + ', '
        #                 END,
        #                 CASE
        #                 WHEN rs.MandatorySkill4 IS NULL
        #                     THEN ''
        #                     ELSE rs.MandatorySkill4 + ', '
        #                 END)), 1, 2, '')) AS RequirementSkills,
        #             Stuff(
        #                 (SELECT DISTINCT ', ' +zm.ZIPCode
        #                 FROM dbo.RequirementMaster rm2
        #                 LEFT JOIN dbo.RequirementLocation rl ON rm2.RequirementID = rl.RequirementID
        #                 LEFT JOIN dbo.RequirementOtherLocation rol ON rm2.RequirementID = rol.RequirementID
        #                 LEFT JOIN dbo.AddressMaster am ON rl.AddressID = am.AddressID OR rol.AddressID = am.AddressID
        #                 LEFT JOIN dbo.ZIPCodeMaster zm ON  am.ZIPCodeID = zm.ZIPCodeID
        #                 WHERE rm.RequirementID = rm2.RequirementID  for xml path ('')),1,1,'') AS RequirementZIPCode,
        #             rm.CreatedDate,
        #             rm.ModifiedDate
        #         FROM
        #             dbo.RequirementMaster rm WITH (NOLOCK)
        #         LEFT JOIN
        #             dbo.JobTitleMaster jtm WITH (NOLOCK) ON rm.JobTitleID = jtm.JobTitleID
        #         LEFT JOIN
        #             dbo.JobTypeMaster jtm2 WITH (NOLOCK) ON rm.JobTypeID = jtm2.JobTypeID
        #         LEFT JOIN
        #             dbo.RequirementVisa rv WITH (NOLOCK) ON rm.RequirementID = rv.RequirementID
        #         LEFT JOIN
        #             dbo.VisaMaster vm WITH (NOLOCK) ON rv.VisaID = vm.VisaID
        #         LEFT JOIN
        #             dbo.RequirementSkill rs WITH (NOLOCK) ON rm.RequirementID = rs.RequirementID
        #         LEFT JOIN
        #             dbo.RequirementStatusTxn rst WITH (NOLOCK) ON rs.RequirementID = rst.RequirementID
        #         WHERE
        #             (rm.CreatedDate > '{0}' OR rm.ModifiedDate BETWEEN '{1}' AND '{2}')
        #         AND
        #             rst.StatusID IN (1,6,10,11)
        #         """.format(last_executed_time, start_modified_time, end_modified_time)
        #
        # df = pd.read_sql_query(query, self.connection)

        column_names = ['RequirementID', 'JobTitle', 'JobType', 'IsRemoteLocation', 'VisaStatus',
                        'RequirementJobDescription', 'ActualRequirement', 'RequirementSkills', 'RequirementZIPCode',
                        'CreatedDate', 'ModifiedDate']

        with self.connection.cursor() as cursor:
            res = cursor.execute("{CALL Usp_ML_Get_RequirementlistByDates (?,?,?)}",
                                 (last_executed_time, start_modified_time, end_modified_time))
            result = res.fetchall()

        result = np.array([np.array(r) for r in result])
        df = pd.DataFrame(result, columns=column_names)

        if 'Unnamed: 0' in df:
            df.drop(labels=['Unnamed: 0'], axis=1, inplace=True)

        return df
