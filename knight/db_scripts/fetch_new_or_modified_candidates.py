__author__ = "Mohit Thakkar"

import os
import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings

from ration.models import TaskExecutionTimings

# Get base directory - 'SmartAI'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FetchNewOrModifiedCandidates:
    def __init__(self):
        self.connection = pyodbc.connect(DRIVER=settings.DB_DRIVER,
                                         SERVER=settings.DB_SERVER,
                                         DATABASE=settings.DB_NAME,
                                         UID=settings.DB_USER,
                                         PWD=settings.DB_PASSWORD)

    def fetch_new_or_modified_candidates(self):
        # Get last executed time for the task
        obj = TaskExecutionTimings.objects.get(task_name='GetCandidateDetails')
        last_executed_time = obj.last_execution_time.replace(tzinfo=None, microsecond=0)

        # query = """
        #                 SELECT TOP 1000
        #                     cm.CandidateID as candidateid,
        #                     cp.PortalName AS source,
        #                     reverse(stuff(reverse(CONCAT(
        #                         CASE
        #                         WHEN cm.Prefix IS NULL
        #                             THEN ''
        #                             ELSE cm.Prefix + ' '
        #                         END,
        #                         CASE
        #                         WHEN cm.FirstName IS NULL
        #                             THEN ''
        #                             ELSE cm.FirstName + ' '
        #                         END,
        #                         CASE
        #                         WHEN cm.MiddleName IS NULL
        #                             THEN ''
        #                             ELSE cm.MiddleName + ' '
        #                         END,
        #                         CASE
        #                         WHEN cm.LastName IS NULL
        #                             THEN ''
        #                             ELSE cm.LastName + ' '
        #                         END)), 1, 1, '')) as candidatename,
        #                     cm.Email as email,
        #                     cm.VerifiedByEmail AS isemailverified,
        #                     cm.Mobile as mobile,
        #                     cm.Birthdate as birthdate,
        #                     ed.TotalYears AS totalexperience,
        #                     ed.USExperience as usexperience,
        #                     cr.ResumeContent as resumecontent,
        #                     jspm.JobSearchPriorityText AS jobsearchstatus,
        #                     red.DegreeName AS highestdegree,
        #                     red.PassingYear as passingyear,
        #                     red.IsGraduate as isgraduate,
        #                     vcs.CandidateSkills as candidateskills,
        #                     zm.ZIPCode as zipcode,
        #                     CASE
        #                         WHEN cm.Relocation IS NULL
        #                             THEN 0
        #                             ELSE cm.Relocation
        #                     END AS willRelocate,
        #                     CASE
        #                         WHEN cm.SSN IS NOT NULL
        #                             THEN 1
        #                             ELSE 0
        #                     END AS isssnavailable,
        #                     vm.VisaName AS visastatus,
        #                     cv.VisaExpiryDate as visaexpirydate,
        #                     cm.CreatedDate as createddate,
        #                     cm.ModifiedDate AS updateddate
        #                 FROM
        #                     dbo.CandidateMaster cm WITH (NOLOCK)
        #                 LEFT JOIN
        #                     dbo.CandidateContactTxn cct WITH (NOLOCK) ON cm.CandidateID = cct.CandidateID
        #                 LEFT JOIN
        #                     dbo.AddressMaster am WITH (NOLOCK) ON cct.AddressID = am.AddressID
        #                 LEFT JOIN
        #                     dbo.ZIPCodeMaster zm WITH (NOLOCK) ON am.ZIPCodeID = zm.ZIPCodeID
        #                 LEFT JOIN
        #                     dbo.CandidatePortal cp WITH (NOLOCK) ON cm.CandidateID = cp.CandidateID
        #                 LEFT JOIN
        #                     dbo.CandidateVisa cv WITH (NOLOCK) ON cm.CandidateID = cv.CandidateID
        #                 LEFT JOIN
        #                     dbo.VisaMaster vm WITH (NOLOCK) ON cv.VisaID = vm.VisaID
        #                 LEFT JOIN
        #                     dbo.CandidateResume cr WITH (NOLOCK) ON cm.CandidateID = cr.CandidateID
        #                 LEFT JOIN
        #                     dbo.ResumeExperiences re WITH (NOLOCK) ON cr.ResumeID = re.ResumeID
        #                 LEFT JOIN
        #                     dbo.ExperienceDetail ed WITH (NOLOCK) ON re.ExperiencesID = ed.ExperiencesID
        #                 LEFT JOIN
        #                     dbo.ExperienceJobTitle ejt WITH (NOLOCK) ON ed.ExperienceDetailID = ejt.ExperienceDetailID
        #                 LEFT JOIN
        #                     dbo.DisplayCandidateResume dcr WITH (NOLOCK) ON cm.CandidateID = dcr.CandidateID
        #                 LEFT JOIN
        #                     dbo.CandidateJobSearchPriority cjsp WITH (NOLOCK) ON cm.CandidateID = cjsp.CandidateID
        #                 LEFT JOIN
        #                     dbo.JobSearchPriorityMaster jspm WITH (NOLOCK) ON cjsp.JobSearchPriorityID = jspm.JobSearchPriorityID
        #                 LEFT JOIN
        #                     dbo.ResumeEducation red WITH (NOLOCK) ON cr.ResumeID = red.ResumeID
        #                 LEFT JOIN
        #                     dbo.vw_CandidateSkills vcs WITH (NOLOCK) ON cm.CandidateID = vcs.CandidateID
        #                 WHERE
        #                     cm.ModifiedDate > '{0}'
        #                 ORDER BY
        #                     cm.ModifiedDate DESC
        #         """.format(last_executed_time)
        #
        # df = pd.read_sql_query(query, self.connection)

        column_names = ['candidateid', 'source', 'candidatename', 'email', 'isemailverified', 'mobile', 'birthdate',
                        'totalexperience', 'usexperience', 'resumecontent', 'jobsearchstatus', 'highestdegree',
                        'passingyear', 'isgraduate', 'candidateskills', 'ZIPCode', 'willRelocate', 'isssnavailable',
                        'visastatus', 'visaexpirydate', 'createddate', 'updateddate']

        with self.connection.cursor() as cursor:
            res = cursor.execute("{CALL Usp_ML_Get_CandidatelistByModifyDate (?)}", (last_executed_time))
            result = res.fetchall()

        result = np.array([np.array(r) for r in result])
        if result:
            df = pd.DataFrame(result, columns=column_names)
        else:
            df = pd.DataFrame(columns=column_names)

        df.drop(columns=list(df.filter(regex='Unnamed:')), inplace=True)

        obj.last_execution_time = make_aware(datetime.now())
        obj.save()
        return df
